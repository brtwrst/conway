#!/usr/bin/env python
""" Conways game of life """
#pylint: disable=E0611
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence

class conwayButton(QPushButton):
    def __init__(self, x, y, p, s):
        super().__init__()
        self._x = x
        self._y = y
        self._parent = p
        self.setFixedSize(s,s)
        self.clicked.connect(self._click)
        self.setStyleSheet("background-color: White")

    def _click(self):
        self._parent.click(self._x, self._y)

class conway(QMainWindow):
    def __init__(self, dim=50, bSize=15, parent=None):
        super().__init__()
        self.dim = dim
        self.bSize = bSize
        self.cells = [[False for _ in range(self.dim)] for _ in range(self.dim)]
        self.gen = 0
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('Press Space to advance')
        self.resize(self.bSize * (self.dim + 1) , self.bSize * (self.dim + 1))
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)

        self.buttons = []
        for i in range(self.dim):
            l=[]
            for j in range(self.dim):
                b=conwayButton(i,j, self, self.bSize)
                l.append(b)
                self.gridLayout.addWidget(b, i, j)
                self.gridLayout.setColumnMinimumWidth(j, self.bSize)
            self.buttons.append(l)
            self.gridLayout.setRowMinimumHeight(i, self.bSize)

        self.shortcutSpace = QShortcut(QKeySequence('space'), self)
        self.shortcutSpace.activated.connect(self.on_spacebar)

    def on_spacebar(self):
        self.evolve()
        self.gen += 1
        self.setWindowTitle(f'Gen {self.gen}')

    def click(self, x=0, y=0):
        self.swap(x,y)

    def swap(self, x, y):
        self.cells[x][y] = not self.cells[x][y]
        self.buttons[x][y].setStyleSheet(
            f'background-color: {"black" if self.cells[x][y] else "white"}'
            )

    def evolve(self):
        before = []
        for x in self.cells:
            before.append(x[:])
        c = 0
        while c < self.dim ** 2:
            x = c // self.dim
            y = c % self.dim
            alive_neighbors = 0
            for dx in range(-1,2):
                if not -1 < x+dx < self.dim:
                    continue
                for dy in range(-1,2):
                    if not -1 < y+dy < self.dim:
                        continue
                    if dy == dx == 0:
                        continue
                    alive_neighbors += before[x+dx][y+dy]

            if before[x][y]:
                if not 1 < alive_neighbors < 4:
                    self.swap(x, y)
            else:
                if alive_neighbors == 3:
                    self.swap(x, y)
            c += 1



def main():
    import sys
    _dim = 0
    _size = 0
    if len(sys.argv) > 1:
        _dim = int(sys.argv[1])
        _size = int(sys.argv[2])
    app = QApplication([])
    window = conway(_dim or 50,_size or 15)
    window.show()
    app.exec_()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
