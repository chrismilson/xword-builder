class XCell:
    def __init__(self, across = None, down = None, char: str = ' '):
        self.char = char[0].upper()
        self.across = across
        self.down = down
        self.count = 0

    def __bool__(self):
        return self.char != ' '

    def set(self, dir: str, value: str):
        char = value[0].upper()

        if dir.upper() in ['F', 'FORCE']:
            self.char = char

        if self and char != self.char:
            raise Exception(f'Word does not fit. Tried entering {char} on {self.char}')

        if len(value) > 1:
            if dir.upper() in ['D', 'DN', 'DOWN']:
                if self.down == None:
                    raise Exception('Out of bounds')
                self.down.set(dir, value[1:])
            elif dir.upper() in ['A', 'ACROSS']:
                if self.across == None:
                    raise Exception('Out of bounds')
                self.across.set(dir, value[1:])
            else:
                return
        self.char = char
        self.count += 1

    def __str__(self):
        if self:
            return self.char
        return '\u2588'

class XRow:
    def __init__(self, size: int, down = None):
        self.size = size
        self.cells = []
        if down:
            self.cells.append(XCell(down = down[size - 1]))
            for i in range(size - 1):
                self.cells.insert(0, XCell(across = self.cells[0], down = down[size - 2 - i]))
        else:
            self.cells.append(XCell())
            for i in range(size - 1):
                self.cells.insert(0, XCell(across = self.cells[0]))

    def __getitem__(self, key):
        return self.cells[key]

    def __setitem__(self, key, value):
        # The direction does not matter, as there is only one character.
        self.cells[key].set('FORCE', value[0])

    def __str__(self):
        val = ''
        for cell in self.cells:
            val += str(cell) + '\t'
        return val

class XWord:
    def __init__(self, size: int):
        self.size = size
        self.rows = []
        self.rows.append(XRow(size))
        for i in range(size - 1):
            self.rows.insert(0, XRow(size, self.rows[0]))

    def __getitem__(self, key):
        return self.rows[key]

    def __str__(self):
        val = ''
        for row in self.rows:
            val += str(row) + '\n\n'
        return val

class XClue:
    def __init__(self, id: int, answer: str, dir: str, clue: str = ''):
        self.id = id
        self.dir = dir
        self.answer = answer
        self.clue = clue
