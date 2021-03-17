from random import choice
import os
import pygame

RED = 255, 0, 0
ORANGE = 255, 155, 0
YELLOW = 255, 255, 0
GREEN = 0, 255, 0
BLUE = 50, 50, 255
PURPLE = 255, 0, 255
WHITE = 255, 255, 255

# Create blocks
blue = pygame.transform.scale(pygame.image.load(os.path.join('images', 'blue.png')), (25, 25))
green = pygame.transform.scale(pygame.image.load(os.path.join('images', 'green.png')), (25, 25))
orange = pygame.transform.scale(pygame.image.load(os.path.join('images', 'orange.png')), (25, 25))
purple = pygame.transform.scale(pygame.image.load(os.path.join('images', 'purple.png')), (25, 25))
red = pygame.transform.scale(pygame.image.load(os.path.join('images', 'red.png')), (25, 25))
teal = pygame.transform.scale(pygame.image.load(os.path.join('images', 'teal.png')), (25, 25))
yellow = pygame.transform.scale(pygame.image.load(os.path.join('images', 'yellow.png')), (25, 25))


class Xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class L:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[0, 1, 0],
                       [0, 2, 0],
                       [1, 1, 0]]
        self.color = orange


class O:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[1, 1],
                       [1, 1]]
        self.color = yellow


class J:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[1, 1, 0],
                       [0, 2, 0],
                       [0, 1, 0]]
        self.color = blue


class I:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[0, 1, 0, 0],
                       [0, 2, 0, 0],
                       [0, 1, 0, 0],
                       [0, 1, 0, 0]]
        self.color = teal


class Z:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[1, 0, 0],
                       [1, 2, 0],
                       [0, 1, 0]]
        self.color = red


class S:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[0, 1, 0],
                       [1, 2, 0],
                       [1, 0, 0]]
        self.color = green


class T:
    def __init__(self, x, y):
        self.ref_x, self.ref_y = x, y
        self.cells = [Xy(x, y), Xy(x, y), Xy(x, y), Xy(x, y)]
        self.matrix = [[0, 1, 0],
                       [1, 2, 0],
                       [0, 1, 0]]
        self.color = purple


class Shape:
    def __init__(self, x, y, x_max, y_max, shapes=None):
        if shapes:
            self.shapes = shapes
            self.shapes.append(choice([O(x, y), L(x, y), J(x, y), I(x, y), Z(x, y), S(x, y), T(x, y)]))
        else:
            self.shapes = []
            for num in range(4):
                self.shapes.append(choice([O(x, y), L(x, y), J(x, y), I(x, y), Z(x, y), S(x, y), T(x, y)]))

        self.cur_shape = self.shapes.pop(0)
        self.refresh()
        self.pivot_x = 0
        self.pivot_y = 0
        self.x_max = x_max
        self.y_max = y_max
        self.color = self.cur_shape.color
        self.held = False
        self.O = O(1, 1)
        self.L = L(1, 1)
        self.J = J(1, 1)
        self.I = I(1, 1)
        self.Z = Z(1, 1)
        self.S = S(1, 1)
        self.T = T(1, 1)

    def refresh(self):
        index = 0
        for num_x in range(len(self.cur_shape.matrix[0])):
            for num_y in range(len(self.cur_shape.matrix[0])):
                if self.cur_shape.matrix[num_x][num_y] != 0:
                    self.cur_shape.cells[index].x = self.cur_shape.ref_x + num_x
                    self.cur_shape.cells[index].y = self.cur_shape.ref_y + num_y

                    # Assign pivot point if available  # TODO remove pivots if no longer needed
                    if self.cur_shape.matrix[num_x][num_y] == 2:
                        self.pivot_x = self.cur_shape.ref_x + num_x
                        self.pivot_y = self.cur_shape.ref_y + num_y

                    index += 1

    def rotate(self, orient):
        if orient == -1:  # Rotate matrix LEFT
            self.cur_shape.matrix = [[self.cur_shape.matrix[j][i] for j in reversed(range(len(self.cur_shape.matrix)))]
                                     for i in range(0, len(self.cur_shape.matrix[0]), 1)]
        else:  # Rotate matrix RIGHT
            self.cur_shape.matrix = [[self.cur_shape.matrix[j][i] for j in range(len(self.cur_shape.matrix))] for i in
                                     range(len(self.cur_shape.matrix[0]) - 1, -1, -1)]
        self.refresh()

    def undo_rotate(self, orient):
        if orient > 0:  # Rotate matrix LEFT
            self.cur_shape.matrix = [
                [self.cur_shape.matrix[j][i] for j in reversed(range(len(self.cur_shape.matrix)))] for i in
                range(0, len(self.cur_shape.matrix[0]), 1)]
        else:  # Rotate matrix RIGHT
            self.cur_shape.matrix = [[self.cur_shape.matrix[j][i] for j in range(len(self.cur_shape.matrix))]
                                     for i in range(len(self.cur_shape.matrix[0]) - 1, -1, -1)]
        self.refresh()

    def rotation_run(self, orient, grid, grid_width, grid_height, dropping_timer):

        ref_x0, ref_y0 = self.cur_shape.ref_x, self.cur_shape.ref_y

        self.rotate(orient)

        test_matrix = [[22, 12, 11, 13, 23],
                       [20, 9, 8, 10, 21],
                       [18, 3, 'p', 4, 19],
                       [16, 1, 0, 2, 17],
                       [14, 6, 5, 5, 15],
                       ]
        test_order = []
        for z in range(len(test_matrix) * len(test_matrix[0])):
            for y in range(len(test_matrix)):
                for x in range(len(test_matrix[0])):
                    if test_matrix[y][x] == z:
                        delta_x = x - 2
                        delta_y = y - 2
                        test_order.append([delta_x, delta_y])

        for z in range(len(test_order)):
            if [True for cell in self.cur_shape.cells if cell.y >= grid_height or cell.x >= grid_width or cell.x < 0 or grid[cell.x][cell.y].rigid]:
                self.cur_shape.ref_x, self.cur_shape.ref_y = ref_x0 + test_order[z][0], ref_y0 + test_order[z][1]
                self.refresh()

                if not [True for cell in self.cur_shape.cells if cell.y >= grid_height or cell.x >= grid_width or cell.x < 0 or grid[cell.x][cell.y].rigid]:
                    dropping_timer = pygame.time.get_ticks()
                    break

        if [True for cell in self.cur_shape.cells if cell.y >= grid_height or cell.x >= grid_width or cell.x < 0 or grid[cell.x][cell.y].rigid]:
            self.cur_shape.ref_x, self.cur_shape.ref_y = ref_x0, ref_y0
            self.refresh()
            self.undo_rotate(orient)  # Undo Rotation

        return dropping_timer

    def move(self, x, y, grid):

        if not self.blocked(x, y, grid):
            self.cur_shape.ref_x += x
            self.cur_shape.ref_y += y
            self.refresh()
            return True

        else:
            # print("blocked")
            return False

    def blocked(self, x, y, grid):
        for cell in self.cur_shape.cells:

            # check for boundary collision on left, right and bottom
            if cell.x + x < 0 or cell.x + x >= self.x_max or cell.y + y >= self.y_max:
                return True

            else:  # it's within boundaries
                # now check for cell collision
                if cell.y + y >= 0:
                    if grid[cell.x + x][cell.y + y].rigid:
                        return True
        return False
