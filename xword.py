class XCell:
    def __init__(self, char: str = ' '):
        self.char = char[0].upper()

    def __bool__(self):
        return self.char != ' '

    def __str__(self):
        if self:
            return self.char
        return '\u2588'

class XRow:
    def __init__(self, size: int):
        self.size = size
        self.cells = []
        for i in range(size):
            self.cells.append(XCell())

    def __getitem__(self, key):
        return self.cells[key]

    def __setitem__(self, key, value):
        self.cells[key] = XCell(value)

    def __str__(self):
        val = ''
        for cell in self.cells:
            val += str(cell) + '\t'
        return val

class XWord:
    def __init__(self, size: int):
        self.size = size
        self.rows = []
        for i in range(size):
            self.rows.append(XRow(size))

    def __getitem__(self, key):
        return self.rows[key]

    def __str__(self):
        val = ''
        for row in self.rows:
            val += str(row) + '\n\n'
        return val
