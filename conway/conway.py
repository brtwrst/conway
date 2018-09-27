#!/usr/bin/env python
""" FOO """
#pylint: disable=E0611
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow

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
        self.resize(900,900)
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)

        self.buttons = []
        for i in range(99):
            l=[]
            for j in range(99):
                b=conwayButton(i,j, self)
                l.append(b)
                self.gridLayout.addWidget(b, i, j)
                self.gridLayout.setColumnMinimumWidth(j, 9)
            self.buttons.append(l)
            self.gridLayout.setRowMinimumHeight(i, 9)

    def click(self, x=0, y=0):
        self.buttons[x][y].setStyleSheet("background-color: black")

def main():
    app = QApplication([])
    window = conway()
    window.show()
    app.exec_()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
