from helpers.DataBaseHelper import get_best_score_top


class Table:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def resize(self, width, height):
        self.width = width
        self.height = height

    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        print([elem for elem in get_best_score_top()])
