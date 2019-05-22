from xword import XWord
from tkinter import *

class XBoard:
    def __init__(self, master, size: int):
        self.tileSize = 30
        self.tileSep = 3

        frame = Frame(master)
        frame.pack(side = 'left')

        self.size = size
        self.board = XWord(size)

        self.canvas = Canvas(frame,
            width = self.tileSize * size + self.tileSep * 2,
            height = self.tileSize * size + self.tileSep * 2
        )
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.onClick)
        self.canvas.bind('<Button-2>', self.resetCells)

        # background
        bg = self.canvas.create_rectangle(
            0,
            0,
            self.tileSize * size + self.tileSep * 2,
            self.tileSize * size + self.tileSep * 2,
            fill = '#444444'
        )

        for i in range(self.size):
            for j in range(self.size):
                cell = self.canvas.create_rectangle(
                    self.tileSize * i + self.tileSep * 2,
                    self.tileSize * j + self.tileSep * 2,
                    self.tileSize * i + self.tileSize + self.tileSep,
                    self.tileSize * j + self.tileSize + self.tileSep,
                    tags = ('cell', 'empty', f'at {j} {i}')
                )

        self.canvas.itemconfig('empty', width = 0, fill = '#000000')

    def onClick(self, event):
        row = event.y // self.tileSize
        col = event.x // self.tileSize

        self.newWord(row, col)

    def resetCells(self, event):
        print('moo')
        self.canvas.addtag_withtag('empty', 'non-empty')
        self.canvas.itemconfig('non-empty', fill = '#000000')
        self.canvas.dtag('non-empty', 'non-empty')

    def newWord(self, row, col):
        # open dialogue to get new word.

        # try to add new word to XWord

        # if good, redraw XBoard
        pass

class XLegend:
    def __init__(self, master, board):
        self.board = board
        self.clues = board.getWords()

        frame = Frame(master)
        frame.pack(side = 'right')

        self.canvas = Canvas(frame, width = 700, height = 100)
        self.canvas.pack()

class XWordBuilder:
    def __init__(self, size: int = 1):
        self.root = Tk()
        self.board = XBoard(self.root, size)

        self.legend = XLegend(self.root, self.board.board)

    def start(self):
        self.root.mainloop()
