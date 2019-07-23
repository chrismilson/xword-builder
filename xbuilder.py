from xword import XWord
from tkinter import *

class XBoard:
    def __init__(self, master, size: int):
        self.tileSize = 30
        self.tileSep = 3
        self.master = master

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

        # open dialogue to get new word.
        dialog = XDialog(self.master, 'New Word')

        if not self.newWord(row, col, dialog.result):
            return

        self.canvas.itemconfig(
            f'at {row} {col}',
            fill = '#ffffff',
            tags = ('cell', 'non-empty', f'at {row} {col}')
        )

    def resetCells(self, event):
        self.canvas.addtag_withtag('empty', 'non-empty')
        self.canvas.itemconfig('non-empty', fill = '#000000')
        self.canvas.dtag('non-empty', 'non-empty')

    def newWord(self, row: int, col: int, result):
        try:
            self.board[row][col].set(result['dir'], result['word'])
            return True
        except:
            print(f'failed at row: {row}, col: {col}')
            return False


class XDialog(Toplevel):
    def __init__(self, master, title = None):
        Toplevel.__init__(self, master)
        self.transient(master)

        if title:
            self.title(title)

        self.parent = master

        self.result = {'dir': 'Across', 'word': ''}

        body = Frame(self)

        self.initial_focus = self.body(body)
        body.pack(padx = 10, pady = 10)

        self.protocol('WM_DELETE_WINDOW', self.cancel)

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self, master):
        bodyFrame = Frame(master)
        bodyFrame.pack()

        wordFrame = Frame(bodyFrame)
        wordFrame.pack(side = TOP)
        wordLabel = Label(wordFrame, text = 'Word')
        wordLabel.pack(side = LEFT)
        wordEntry = Entry(wordFrame)
        wordEntry.pack(side = LEFT)

        dirFrame = Frame(bodyFrame)
        dirFrame.pack(side = TOP)
        acrossRadio = Radiobutton(
            dirFrame,
            text = 'Across',
            variable = self.result['dir'],
            value = 'Across',
            indicatoron = False
        )
        downRadio = Radiobutton(
            dirFrame,
            text = 'Down',
            variable = self.result['dir'],
            value = 'Down',
            indicatoron = False
        )
        acrossRadio.pack(side = LEFT)
        downRadio.pack(side = RIGHT)
        acrossRadio.select()

        return wordEntry


    def cancel(self, event = None):
        self.master.focus_set()
        self.destroy()

    def apply(self):
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
    def __init__(self, size: int = 1, xword = None):
        self.root = Tk()
        if xword:
            self.board = XBoard(self.root, xword = xword)
        self.board = XBoard(self.root, size)

        self.legend = XLegend(self.root, self.board.board)

    def start(self):
        self.root.mainloop()
