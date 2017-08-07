from collections import OrderedDict

UL, UR, DL, DR = 'u', 'y', 'e', 'i'

class Cell(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def divide(self):
        return OrderedDict(((c, self.newCell(i)) for i, c in enumerate((UL, UR, DL, DR))))


    def newCell(self, i):
        gridX = i % 2
        gridY = i // 2
        cellW = self.w // 2
        cellH = self.h // 2
        cellX = self.x + cellW * gridX
        cellY = self.y + cellH * gridY
        # print(cellX, cellY, cellW, cellH, i, self.x, self.y, self.w, self.h)
        return Cell(cellX, cellY, cellW, cellH)