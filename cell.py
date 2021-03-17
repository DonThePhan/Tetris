class Cell:
    def __init__(self, rect, color):
        self.color_initial = color
        self.rect = rect
        self.color = self.color_initial
        self.rigid = False

