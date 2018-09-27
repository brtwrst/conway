#!/usr/bin/env python
""" Conways game of life """
#pylint: disable=E0611
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QGridLayout
from PyQt5.QtWidgets import QMainWindow, QShortcut, QAction, qApp, QStyleFactory
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QKeySequence, QIcon
import json
import sys
import os


class conwayButton(QPushButton):
    def __init__(self, x, y, p, s):
        super().__init__()
        self._x = x
        self._y = y
        self._parent = p
        self.setFixedSize(s, s)
        self.clicked.connect(self._click)
        self.setStyleSheet("background-color: White")

    def _click(self):
        self._parent.click(self._x, self._y)


class conway(QMainWindow):
    def __init__(self, dim=50, bSize=15, parent=None):
        super().__init__()
        self.dim = dim
        self.bSize = bSize
        self.cells = [[False for _ in range(self.dim)]
                      for _ in range(self.dim)]
        self.gen = 0
        self.setupUI()
        self.setupMenu()
        # self.help_popup()

    def setupUI(self):
        self.setWindowTitle('Press Space to advance')
        self.resize(self.bSize * (self.dim + 1), self.bSize * (self.dim + 1))
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)

        self.buttons = []
        for i in range(self.dim):
            l = []
            for j in range(self.dim):
                b = conwayButton(i, j, self, self.bSize)
                l.append(b)
                self.gridLayout.addWidget(b, i, j)
                self.gridLayout.setColumnMinimumWidth(j, self.bSize)
            self.buttons.append(l)
            self.gridLayout.setRowMinimumHeight(i, self.bSize)

    def setupMenu(self):
        self.shortcutSpace = QShortcut(QKeySequence('space'), self)
        self.shortcutSpace.activated.connect(self.on_spacebar)

        menubar = self.menuBar()

        saveAct = QAction('&Save', self)
        saveAct.triggered.connect(self._save)
        menubar.addAction(saveAct)

        loadAct = QAction('&Load', self)
        loadAct.triggered.connect(self._load)
        menubar.addAction(loadAct)

        template_menu = menubar.addMenu('&Templates')

        templateSimple = QAction('&SimpleGliders', self)
        templateSimple.triggered.connect(self._setupSimple)
        template_menu.addAction(templateSimple)

        templateActDGG = QAction('&DoubleGliderGun + Catchers', self)
        templateActDGG.triggered.connect(self._setupDGG)
        template_menu.addAction(templateActDGG)

        templateActMGG = QAction('&QuadGliderGun - No Catchers', self)
        templateActMGG.triggered.connect(self._setupMGG)
        template_menu.addAction(templateActMGG)

        templateActVirus = QAction('&Viruses', self)
        templateActVirus.triggered.connect(self._setupViruses)
        template_menu.addAction(templateActVirus)

        templateActEM = QAction('&EM', self)
        templateActEM.triggered.connect(self._setupEM)
        template_menu.addAction(templateActEM)

        clearAct = QAction('&Reset', self)
        clearAct.triggered.connect(self._clear)
        menubar.addAction(clearAct)

        helpAct = QAction('&Help', self)
        helpAct.triggered.connect(self.help_popup)
        menubar.addAction(helpAct)

        exitAct = QAction('&Exit', self)
        exitAct.triggered.connect(qApp.quit)
        menubar.addAction(exitAct)

    def help_popup(self):
        _ = QMessageBox.information(
            self, 'Rules',
            'Any live cell with fewer than two live neighbors dies, '+
            'as if by under population.\n'+
            'Any live cell with two or three live neighbors lives on '+
            'to the next generation.\n'+
            'Any live cell with more than three live neighbors dies, '+
            'as if by overpopulation.\n'+
            'Any dead cell with exactly three live neighbors becomes '+
            'a live cell, as if by reproduction.'+
            '\n\nClick to toggle a cell between dead/alive.'
            '\nUse Spacebar to advance one generation.',
            QMessageBox.Ok
            )

    def _save(self):
        with open(f'saved.json', 'w') as f:
            json.dump([self.cells, self.gen, self.dim,
                       self.bSize], f, indent=1)

    def _load(self):
        if os.path.isfile('saved.json'):
            self._loadgame('saved')

    def _loadgame(self, game='saved'):
        with open(f'{game}.json') as f:
            self.cells, self.gen, self.dim, self.bSize = json.load(f)
        self.setupUI()
        for sub_cell, sub_btn in zip(self.cells, self.buttons):
            for cell, btn in zip(sub_cell, sub_btn):
                btn.setStyleSheet(
                    f'background-color: {"black" if cell else "white"}'
                )
        self.setWindowTitle(f'Gen {self.gen}')

    def _setupSimple(self):
        self._loadgame('simple')

    def _setupEM(self):
        self._loadgame('em')

    def _setupDGG(self):
        self._loadgame('dgg')

    def _setupMGG(self):
        self._loadgame('mgg')

    def _setupViruses(self):
        self._loadgame('viruses')

    def _clear(self):
        self.cells = [[False for _ in range(self.dim)]
                      for _ in range(self.dim)]
        for b_row in self.buttons:
            for b in b_row:
                b.setStyleSheet("background-color: White")
        self.gen = 0
        self.setWindowTitle('Press Space to advance')

    def on_spacebar(self):
        self.evolve()
        self.gen += 1
        self.setWindowTitle(f'Gen {self.gen}')

    def click(self, x=0, y=0):
        self.swap(x, y)

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
            for dx in range(-1, 2):
                if not -1 < x+dx < self.dim:
                    continue
                for dy in range(-1, 2):
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
    _dim = 0
    _size = 0
    if len(sys.argv) > 1:
        _dim = int(sys.argv[1])
        _size = int(sys.argv[2])
    app = QApplication([])
    # print(QStyleFactory.keys())
    app.setStyle(QStyleFactory.create('Windows'))
    window = conway(_dim or 50, _size or 15)
    window.show()
    app.exec_()


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
