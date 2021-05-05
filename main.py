import pygame
from cell import Cell
from shape import Shape
import os

pygame.init()

START_X, START_Y = 3, 0
PADDING = 30
FPS = 60
CLOCK = pygame.time.Clock()
STARTING_GAME_SPEED = 1000  # milliseconds for block movements interval
STARTING_BUTTON_SPEED = 150  # milliseconds
TETRIS_PREFIX = ['', 'DOUBLE', 'TRIPLE', 'QUADRA', 'PENTA']

# sounds
pygame.mixer.init()
sound_rotate = pygame.mixer.Sound('audio/se_game_rotate.wav')
sound_single = pygame.mixer.Sound('audio/se_game_single.wav')
sound_double = pygame.mixer.Sound('audio/se_game_double.wav')
sound_triple = pygame.mixer.Sound('audio/se_game_triple.wav')
sound_tetris = pygame.mixer.Sound('audio/se_game_tetris.wav')
sound_hold = pygame.mixer.Sound('audio/se_game_hold.wav')
sound_move = pygame.mixer.Sound('audio/se_game_move.wav')
sound_soft_drop = pygame.mixer.Sound('audio/se_game_softdrop.wav')
sound_hard_drop = pygame.mixer.Sound('audio/se_game_harddrop.wav')
sound_count = pygame.mixer.Sound('audio/se_game_count.wav')
sound_game_over = pygame.mixer.Sound('audio/382310__myfox14__game-over-arcade.wav')
sound_level_up = pygame.mixer.Sound('audio/me_game_plvup.wav')

# colors
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = 150, 150, 150
LIGHT_GREY = 200, 200, 200
GRID_BG_COLOR = BLACK
RED = 255, 0, 0
ORANGE = 255, 155, 0
YELLOW = 255, 255, 0
GREEN = 0, 255, 0
BLUE = 50, 50, 255
PURPLE = 255, 0, 255
DARK_GREY = 50, 50, 50

# triple and tetris animation
animation_lines = 0
animation_count_down = 50

# text
pygame.font.init()
FONT_SIZE_30 = pygame.font.Font('baveuse.ttf', 30)
FONT_SIZE_40 = pygame.font.Font('baveuse.ttf', 40)
FONT_SIZE_50 = pygame.font.Font('baveuse.ttf', 40)
FONT_SIZE_60 = pygame.font.Font('baveuse.ttf', 60)
FONT_SIZE_70 = pygame.font.Font('baveuse.ttf', 60)
FONT_SIZE_80 = pygame.font.Font('baveuse.ttf', 60)
text_HOLD = FONT_SIZE_40.render("HOLD", True, WHITE)
text_NEXT = FONT_SIZE_40.render("NEXT", True, WHITE)
text_heading_SCORE = FONT_SIZE_30.render("SCORE", True, WHITE)
text_heading_LEVEL = FONT_SIZE_30.render("LEVEL", True, WHITE)
text_heading_LINES = FONT_SIZE_30.render("LINES", True, WHITE)
text_GAME = FONT_SIZE_60.render("GAME", True, WHITE)
text_OVER = FONT_SIZE_60.render("OVER", True, WHITE)
text_TETRIS_PREFIX = FONT_SIZE_50.render("", True, WHITE)
text_TETRIS = FONT_SIZE_50.render("TETRIS!", True, WHITE)
text_Triple = FONT_SIZE_40.render("Triple", True, WHITE)
text_Double = FONT_SIZE_30.render("Double", True, WHITE)
text_Restart = FONT_SIZE_50.render("Restart", True, WHITE)
text_Pause = FONT_SIZE_80.render("Pause", True, WHITE)
text_Play = FONT_SIZE_50.render("Play", True, WHITE)

# grid specs
CEL_DIM = 25
HOLD_X = 6
MAIN_X = 10
MAIN_Y = 20
NEXT_X = 6

SCREEN_WIDTH = PADDING * 4 + (MAIN_X + HOLD_X + NEXT_X) * (CEL_DIM + 1)
SCREEN_HEIGHT = PADDING * 3 + MAIN_Y * (CEL_DIM + 1)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# buttons
mouse_over_pause_play = False
pause_play = pygame.transform.scale(pygame.image.load(os.path.join('images', 'pause_play.png')), (50, 50))
pause_play_bg = pygame.Rect(SCREEN_WIDTH - pause_play.get_width() - PADDING * 1.5,
                            SCREEN_HEIGHT - pause_play.get_height() - PADDING * 1.5,
                            pause_play.get_width() + PADDING, pause_play.get_height() + PADDING)

# resettable variables at start/restart_game():
game_on = True
game_speed = 0
button_speed = 0
score = 0
level = 0
total_lines = 0
dropping_timer = 0
hold_grid = []
main_grid = []
next_grid = []
restart_rect = pygame.Rect(0, 0, text_Restart.get_width() + PADDING, text_Restart.get_height() + PADDING)
first_shape_null = True
consecutive_tetris = 0
pause = False


def draw(shape, hold_pc, *args):
    global animation_count_down, text_TETRIS_PREFIX
    SCREEN.fill(DARK_GREY)

    SCREEN.blit(text_HOLD,
                (hold_grid[0][0].rect.x + int(HOLD_X / 2) * (CEL_DIM + 1) - text_HOLD.get_width() / 2, PADDING - 10))
    SCREEN.blit(text_NEXT,
                (next_grid[0][0].rect.x + int(HOLD_X / 2) * (CEL_DIM + 1) - text_NEXT.get_width() / 2, PADDING - 10))

    score_text = FONT_SIZE_30.render(str(score), True, WHITE)
    level_text = FONT_SIZE_30.render(str(level), True, WHITE)
    lines_text = FONT_SIZE_30.render(str(total_lines), True, WHITE)

    SCREEN.blit(text_heading_SCORE, (
        hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - text_heading_SCORE.get_width() / 2,
        hold_grid[0][-1].rect.y + (PADDING + 5) * 2))
    SCREEN.blit(score_text, (hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - score_text.get_width() / 2,
                             hold_grid[0][-1].rect.y + (PADDING + 5) * 3))
    SCREEN.blit(text_heading_LEVEL, (
        hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - text_heading_LEVEL.get_width() / 2,
        hold_grid[0][-1].rect.y + (PADDING + 5) * 5))
    SCREEN.blit(level_text, (hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - level_text.get_width() / 2,
                             hold_grid[0][-1].rect.y + (PADDING + 5) * 6))
    SCREEN.blit(text_heading_LINES, (
        hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - text_heading_LINES.get_width() / 2,
        hold_grid[0][-1].rect.y + (PADDING + 5) * 8))
    SCREEN.blit(lines_text, (hold_grid[0][-1].rect.x + HOLD_X / 2 * CEL_DIM - lines_text.get_width() / 2,
                             hold_grid[0][-1].rect.y + (PADDING + 5) * 9))

    # draw the HOLD grid
    for col in hold_grid:
        for cell in col:
            pygame.draw.rect(SCREEN, GRID_BG_COLOR, cell.rect)

    # draw the MAIN grid & grounded pcs
    for col in main_grid:
        for cell in col:
            if not cell.rigid:
                pygame.draw.rect(SCREEN, GRID_BG_COLOR, cell.rect)
            else:
                SCREEN.blit(cell.color, (cell.rect.x, cell.rect.y))

    # draw the NEXT grid
    for col in next_grid:
        for cell in col:
            pygame.draw.rect(SCREEN, GRID_BG_COLOR, cell.rect)

    # draw borders
    pygame.draw.lines(SCREEN, GREY, True, [(hold_grid[0][0].rect.x - 3, hold_grid[0][0].rect.y - 3),
                                           (hold_grid[-1][0].rect.x + CEL_DIM + 2, hold_grid[0][0].rect.y - 3),
                                           (hold_grid[-1][0].rect.x + CEL_DIM + 2,
                                            hold_grid[-1][-1].rect.y + CEL_DIM + 2),
                                           (hold_grid[0][0].rect.x - 3, hold_grid[-1][-1].rect.y + CEL_DIM + 2)
                                           ], 3)

    pygame.draw.lines(SCREEN, GREY, True, [(main_grid[0][0].rect.x - 3, main_grid[0][0].rect.y - 3),
                                           (main_grid[-1][0].rect.x + CEL_DIM + 2, main_grid[0][0].rect.y - 3),
                                           (main_grid[-1][0].rect.x + CEL_DIM + 2,
                                            main_grid[-1][-1].rect.y + CEL_DIM + 2),
                                           (main_grid[0][0].rect.x - 3, main_grid[-1][-1].rect.y + CEL_DIM + 2)
                                           ], 3)

    pygame.draw.lines(SCREEN, GREY, True, [(next_grid[0][0].rect.x - 3, next_grid[0][0].rect.y - 3),
                                           (next_grid[-1][0].rect.x + CEL_DIM + 2, next_grid[0][0].rect.y - 3),
                                           (next_grid[-1][0].rect.x + CEL_DIM + 2,
                                            next_grid[-1][-1].rect.y + CEL_DIM + 2),
                                           (next_grid[0][0].rect.x - 3, next_grid[-1][-1].rect.y + CEL_DIM + 2)
                                           ], 3)

    # draw the HOLD shape with the same hold cells
    if hold_pc:
        for hold_cell in hold_pc.cur_shape.cells:
            cell = hold_grid[hold_cell.x][hold_cell.y]
            cell.color = hold_pc.color
            # pygame.draw.rect(SCREEN, cell.color, cell.rect)
            SCREEN.blit(cell.color, (cell.rect.x, cell.rect.y))

    # draw the current shape with the same grid cells
    if not first_shape_null:
        for shape_cell in shape.cur_shape.cells:
            if shape_cell.y >= 0:
                cell = main_grid[shape_cell.x][shape_cell.y]
                cell.color = shape.color
                SCREEN.blit(cell.color, (cell.rect.x, cell.rect.y))

    # draw next shapes
    shape_num = 0
    for next_shape in shape.shapes:
        index = 0
        for num_x in range(len(next_shape.matrix[0])):
            for num_y in range(len(next_shape.matrix[0])):
                if next_shape.matrix[num_x][num_y] != 0:
                    next_shape.cells[index].x = num_x + 1
                    next_shape.cells[index].y = num_y + shape_num * 3 + 1
                    index += 1
        shape_num += 1
    for next_shape in shape.shapes:
        for shape_cell in next_shape.cells:
            cell = next_grid[shape_cell.x][shape_cell.y]
            cell.color = next_shape.color
            # pygame.draw.rect(SCREEN, cell.color, cell.rect)
            SCREEN.blit(cell.color, (cell.rect.x, cell.rect.y))

    if animation_count_down:
        if animation_lines == 4:
            SCREEN.blit(text_TETRIS, (
                main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - text_TETRIS.get_width() / 2,
                main_grid[0][-1].rect.y - 9 * (CEL_DIM + 1) - (50 - animation_count_down)))
            SCREEN.blit(text_TETRIS_PREFIX, (
                main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - text_TETRIS_PREFIX.get_width() / 2,
                main_grid[0][-1].rect.y - 9 * (CEL_DIM + 1) - (50 - animation_count_down) - text_TETRIS.get_height()))

        elif animation_lines == 3:
            SCREEN.blit(text_Triple, (
                main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - text_Triple.get_width() / 2,
                main_grid[0][-1].rect.y - 9 * (CEL_DIM + 1) - (50 - animation_count_down)))
        animation_count_down -= 1

    # draw pause/play button
    if mouse_over_pause_play:
        pygame.draw.rect(SCREEN, GREY, pause_play_bg)
    SCREEN.blit(pause_play,
                (SCREEN_WIDTH - pause_play.get_width() - PADDING, SCREEN_HEIGHT - pause_play.get_height() - PADDING))

    if pause:
        SCREEN.blit(text_Pause, (
            main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - text_Pause.get_width() / 2,
            main_grid[0][8].rect.y))

    if 'countdown' not in args:
        pygame.display.update()


def ground_shape(shape):
    global game_on

    for cell in shape.cur_shape.cells:
        if cell.y >= 0:
            main_grid[cell.x][cell.y].rigid = True
            main_grid[cell.x][cell.y].color = shape.color
            print(cell.x, cell.y)
        else:
            # When any cell stacks above the grid
            game_on = False


def create_new_shape(shape=None, *args):
    global dropping_timer, consecutive_tetris, text_TETRIS_PREFIX
    dropping_timer = pygame.time.get_ticks()

    if shape:
        if 'first hold' not in args:
            # First time you hold, there is now part in the hold section you we make a new part.
            # But we don't want to ground the last part so we skip this step.
            # It's specific for every other instance except when swapping for the first time.
            if not first_shape_null:
                ground_shape(shape)
                print('grounded')
        shape = Shape(START_X, START_Y, MAIN_X, MAIN_Y, shapes=shape.shapes)
        shape = new_shape_interference_check(shape)

    else:
        shape = Shape(START_X, START_Y, MAIN_X, MAIN_Y)

    # Check Lines, Remove them and animate
    lines = check_for_lines()

    update_game_info(lines)

    return shape


def update_game_info(lines):
    global score, total_lines, level, game_speed, button_speed
    score += 100 * (len(lines) + max(0, (consecutive_tetris - 1))) ** 2
    total_lines += len(lines)
    if level != 1 + total_lines // 10:
        sound_level_up.play()
    level = 1 + total_lines // 10
    game_speed = STARTING_GAME_SPEED * .9 ** (level - 1)
    button_speed = STARTING_BUTTON_SPEED * .95 ** (level - 1)


def new_shape_interference_check(shape):
    while [True for cell in shape.cur_shape.cells if cell.y >= 0 and main_grid[cell.x][cell.y].rigid]:
        shape.cur_shape.ref_y -= 1
        shape.refresh()
    return shape


def check_for_lines():
    global consecutive_tetris, text_TETRIS_PREFIX
    lines = []
    for y in range(MAIN_Y):
        line = True
        for x in range(MAIN_X):
            if not main_grid[x][y].rigid:
                line = False
        if line:
            lines.append(y)

    if lines:
        remove_lines(lines)
    if len(lines) == 4:
        consecutive_tetris += 1
        text_TETRIS_PREFIX = FONT_SIZE_50.render(TETRIS_PREFIX[consecutive_tetris - 1], True, WHITE)
    else:
        consecutive_tetris = 0

    return lines


def remove_lines(lines):
    global main_grid, text_TETRIS_PREFIX, animation_lines, animation_count_down
    delay = 4

    # play sound
    if len(lines) > 3:
        sound_tetris.play()
    elif len(lines) > 2:
        sound_triple.play()
    elif len(lines) > 1:
        sound_double.play()
    else:
        sound_single.play()

    # play line animation (text animation happens in draw())
    for count in range(delay - 2):
        for col in main_grid:
            for y_remove in lines:
                pygame.draw.rect(SCREEN, (200, 200, 200), col[y_remove].rect)
        pygame.display.update()
        pygame.time.delay(int(40 * (delay - count) / delay))

        for col in main_grid:
            for y_remove in lines:
                SCREEN.blit(col[y_remove].color, (col[y_remove].rect.x, col[y_remove].rect.y))
        pygame.display.update()
        pygame.time.delay(int(40 * (delay - count) / delay))

    # set animation properties for 'Tetris' text in draw()
    if len(lines) > 2:
        animation_lines = len(lines)
        animation_count_down = 50

    # bring all cells above line down
    for y_remove in lines:
        for y in reversed(range(1, y_remove + 1)):
            for x in range(MAIN_X):
                main_grid[x][y].rigid = main_grid[x][y - 1].rigid
                main_grid[x][y].color = main_grid[x][y - 1].color

        # for the top line since it has no cells to reference
        for x in range(MAIN_X):
            main_grid[x][0].rigid = False
            main_grid[x][0].color = GRID_BG_COLOR


def start_count_down(shape, hold_pc):
    pygame.mixer.music.load('audio/Tetris 99 Theme.mp3')

    for count_down_num in (range(3, 0, -1)):
        sound_count.play()
        for font_size in range(125, 75, -1):
            if count_down_num == 1 and font_size == 115:
                pygame.mixer.music.play(loops=-1)

            CLOCK.tick(FPS)
            count_down_font = pygame.font.Font('baveuse.ttf', font_size).render(str(count_down_num), True, WHITE)
            count_down_font.set_alpha(255 - (125 - font_size) / 50 * 255)
            draw(shape, hold_pc, 'countdown')

            SCREEN.blit(count_down_font, (main_grid[5][int(MAIN_Y / 3)].rect.x - count_down_font.get_width() / 2,
                                          main_grid[5][int(MAIN_Y / 3)].rect.y))
            pygame.display.update()
            pygame.time.delay(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()


def pause_game(shape, hold_pc):
    global pause, mouse_over_pause_play
    pause = True
    draw(shape, hold_pc)
    pygame.mixer.music.pause()

    while pause:
        CLOCK.tick(FPS)

        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        mouse_over_pause_play = SCREEN_WIDTH - PADDING - pause_play.get_width() < mouse_x < SCREEN_WIDTH - PADDING and \
                                SCREEN_HEIGHT - PADDING - pause_play.get_height() < mouse_y < SCREEN_HEIGHT - PADDING

        if mouse_over_pause_play:
            pygame.draw.rect(SCREEN, GREY, pause_play_bg)
            SCREEN.blit(pause_play,
                        (SCREEN_WIDTH - pause_play.get_width() - PADDING,
                         SCREEN_HEIGHT - pause_play.get_height() - PADDING))
            pygame.display.update()
        else:
            pygame.draw.rect(SCREEN, DARK_GREY, pause_play_bg)
            SCREEN.blit(pause_play,
                        (SCREEN_WIDTH - pause_play.get_width() - PADDING,
                         SCREEN_HEIGHT - pause_play.get_height() - PADDING))
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_over_pause_play or event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = False

    pygame.mixer.music.unpause()


def main():
    global dropping_timer, animation_lines, animation_count_down, first_shape_null, mouse_over_pause_play
    shape = create_new_shape()
    hold_pc = None
    action_timer = pygame.time.get_ticks()

    start_count_down(shape, hold_pc)
    shape = create_new_shape(shape)
    first_shape_null = False

    while game_on:
        CLOCK.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        mouse_over_pause_play = SCREEN_WIDTH - PADDING - pause_play.get_width() < mouse_x < SCREEN_WIDTH - PADDING and SCREEN_HEIGHT - PADDING - pause_play.get_height() < mouse_y < SCREEN_HEIGHT - PADDING

        # if mouse_over_pause_play:
        #     pygame.draw.rect(SCREEN, GREY, pause_play_bg)
        #     SCREEN.blit(pause_play,
        #                 (SCREEN_WIDTH - pause_play.get_width() - PADDING,
        #                  SCREEN_HEIGHT - pause_play.get_height() - PADDING))
        #     pygame.display.update()
        # else:
        #     pygame.draw.rect(SCREEN, DARK_GREY, pause_play_bg)
        #     SCREEN.blit(pause_play,
        #                 (SCREEN_WIDTH - pause_play.get_width() - PADDING,
        #                  SCREEN_HEIGHT - pause_play.get_height() - PADDING))
        #     pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_over_pause_play or event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_game(shape, hold_pc)

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    sound_move.play()
                    action_timer = pygame.time.get_ticks()
                    shape.move(-1, 0, main_grid)
                elif event.key == pygame.K_RIGHT:
                    sound_move.play()
                    action_timer = pygame.time.get_ticks()
                    shape.move(1, 0, main_grid)
                if event.key == pygame.K_DOWN:
                    sound_move.play()
                    action_timer = pygame.time.get_ticks()
                    if not shape.move(0, 1, main_grid):
                        sound_soft_drop.play()
                        shape = create_new_shape(shape)
                    else:
                        dropping_timer = pygame.time.get_ticks()

                if event.key == pygame.K_SPACE:
                    sound_hard_drop.play()
                    while shape.move(0, 1, main_grid):
                        pass
                    shape = create_new_shape(shape)

                if event.key == pygame.K_z:  # Rotate RIGHT
                    dropping_timer = shape.rotation_run(-1, main_grid, MAIN_X, MAIN_Y, dropping_timer)
                    sound_rotate.play()
                elif event.key == pygame.K_x or event.key == pygame.K_UP:  # Rotate LEFT
                    dropping_timer = shape.rotation_run(1, main_grid, MAIN_X, MAIN_Y, dropping_timer)
                    sound_rotate.play()

                if event.key == pygame.K_LCTRL:  # Hold pc
                    sound_hold.play()
                    if not hold_pc:  # First Time in game
                        shape.held = True
                        hold_pc = shape
                        exec(f'hold_pc.cur_shape = hold_pc.{str(hold_pc.cur_shape)[7]}')  # reset block orientation
                        hold_pc.cur_shape.ref_x, hold_pc.cur_shape.ref_y = 1, 1
                        hold_pc.refresh()
                        hold_pc.held = True
                        shape = create_new_shape(shape, 'first hold')
                        shape.held = True
                    else:
                        if not shape.held:
                            shape.held = True
                            hold_pc, shape = shape, hold_pc
                            exec(f'hold_pc.cur_shape = hold_pc.{str(hold_pc.cur_shape)[7]}')  # reset block orientation
                            hold_pc.cur_shape.ref_x, hold_pc.cur_shape.ref_y = 1, 1
                            hold_pc.refresh()
                            shape.cur_shape.ref_x, shape.cur_shape.ref_y = START_X, START_Y
                            shape.refresh()

        if pygame.time.get_ticks() - action_timer > button_speed:
            action_timer = pygame.time.get_ticks()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                sound_move.play()
                shape.move(-1, 0, main_grid)
            elif keys[pygame.K_RIGHT]:
                sound_move.play()
                shape.move(1, 0, main_grid)
            if keys[pygame.K_DOWN]:
                sound_move.play()
                if not shape.move(0, 1, main_grid):
                    sound_soft_drop.play()
                    shape = create_new_shape(shape)
                else:
                    dropping_timer = pygame.time.get_ticks()

        if pygame.time.get_ticks() - dropping_timer > game_speed:
            dropping_timer = pygame.time.get_ticks()

            if not shape.move(0, 1, main_grid):
                sound_soft_drop.play()
                shape = create_new_shape(shape)

        draw(shape, hold_pc)

        if not game_on:
            game_over_screen()


def game_over_screen():
    pygame.mixer.music.stop()
    sound_game_over.play()

    SCREEN.blit(text_GAME,
                (main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - int(text_GAME.get_width() / 2),
                 main_grid[0][0].rect.y + int(MAIN_Y / 2) * (CEL_DIM + 1) - text_GAME.get_height()))
    SCREEN.blit(text_OVER,
                (main_grid[0][0].rect.x + int(MAIN_X / 2) * (CEL_DIM + 1) - int(text_GAME.get_width() / 2),
                 main_grid[0][0].rect.y + int(MAIN_Y / 2) * (CEL_DIM + 1)))

    pygame.draw.rect(SCREEN, DARK_GREY, restart_rect, border_radius=10)
    pygame.draw.rect(SCREEN, GREY, restart_rect, width=2, border_radius=10)
    SCREEN.blit(text_Restart, (restart_rect.x + restart_rect.width / 2 - text_Restart.get_width() / 2,
                               restart_rect.y + restart_rect.height / 2 - text_Restart.get_height() / 2))

    pygame.display.update()

    while True:
        CLOCK.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        mouse_over_restart = \
            restart_rect.x < mouse_x < restart_rect.x + restart_rect.width and \
            restart_rect.y < mouse_y < restart_rect.y + restart_rect.height

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_over_restart:
                    restart_game()


def restart_game():
    global game_on, game_speed, button_speed, score, level, total_lines, dropping_timer, hold_grid, main_grid, next_grid, restart_rect, first_shape_null

    game_on = True
    game_speed = STARTING_GAME_SPEED
    button_speed = STARTING_BUTTON_SPEED
    score = 0
    level = 1
    total_lines = 0
    dropping_timer = pygame.time.get_ticks()
    first_shape_null = True

    hold_grid = []
    for cell_x in range(HOLD_X):
        column = []
        for cell_y in range(4):
            rect = pygame.Rect(cell_x * (CEL_DIM + 1) + PADDING,
                               (cell_y + 2) * (CEL_DIM + 1) + PADDING, CEL_DIM, CEL_DIM)
            column.append(Cell(rect=rect, color=GRID_BG_COLOR))
        hold_grid.append(column)

    main_grid = []
    for cell_x in range(MAIN_X):
        column = []
        for cell_y in range(MAIN_Y):
            rect = pygame.Rect(cell_x * (CEL_DIM + 1) + PADDING + (hold_grid[-1][0].rect.x + CEL_DIM),
                               cell_y * (CEL_DIM + 1) + PADDING, CEL_DIM, CEL_DIM)
            column.append(Cell(rect=rect, color=GRID_BG_COLOR))
        main_grid.append(column)

    next_grid = []
    for cell_x in range(NEXT_X):
        column = []
        for cell_y in range(10):
            rect = pygame.Rect(cell_x * (CEL_DIM + 1) + PADDING + (main_grid[-1][0].rect.x + CEL_DIM),
                               (cell_y + 2) * (CEL_DIM + 1) + PADDING, CEL_DIM, CEL_DIM)
            column.append(Cell(rect=rect, color=GRID_BG_COLOR))
        next_grid.append(column)

    restart_rect = pygame.Rect(main_grid[5][15].rect.x - restart_rect.width / 2, main_grid[5][15].rect.y,
                               restart_rect.width, restart_rect.height)

    main()


if __name__ == '__main__':
    restart_game()
