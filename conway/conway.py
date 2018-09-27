#!/usr/bin/env python
""" FOO """
#pylint: disable=E0611
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QShortcut
from PyQt5.QtGui import QKeySequence

class conwayButton(QPushButton):
    def __init__(self, x, y, p):
        super().__init__()
        self._x = x
        self._y = y
        self._parent = p
        self.buttonSetup()

    def buttonSetup(self):
        self.setFixedSize(9,9)
        self.clicked.connect(self._click)
        self.setStyleSheet("background-color: White")

    def _click(self):
        self._parent.click(self._x, self._y)

class conway(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.dim = 99
        self.size = 9
        self.cells = [[0 for _ in range(99)] for _ in range(99)]

        self.setupUI()

    def setupUI(self):
        self.resize(self.size * 100, self.size* 100)
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)

        self.buttons = []
        for i in range(self.dim):
            l=[]
            for j in range(self.dim):
                b=conwayButton(i,j, self)
                l.append(b)
                self.gridLayout.addWidget(b, i, j)
                self.gridLayout.setColumnMinimumWidth(j, self.size)
            self.buttons.append(l)
            self.gridLayout.setRowMinimumHeight(i, self.size)

        self.shortcutSpace = QShortcut(QKeySequence('space'), self)
        self.shortcutSpace.activated.connect(self.on_spacebar)

    def on_spacebar(self):
        print('SPAAACE')
        # self.shortcutSpace.activated.disconnect()

    def click(self, x=0, y=0):
        self.cells[x][y] = not self.cells[x][y]
        # self.buttons[x][y].setStyleSheet("background-color: black")
        self.draw(x,y)

    def draw(self, x, y):
        self.buttons[x][y].setStyleSheet(
            f'background-color: {"black" if self.cells[x][y] else "white"}'
            )


def main():
    app = QApplication([])
    window = conway()
    window.show()
    app.exec_()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
