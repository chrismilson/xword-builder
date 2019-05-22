class XCell:
    def __init__(self, across = None, down = None, char: str = ' '):
        self.char = char[0].upper()
        self.across = across
        self.down = down
        self.hasDown = False
        self.hasAcross = False

    def __bool__(self):
        return self.char != ' '

    def set(self, dir: str, value: str):
        char = value[0].upper()

        if dir.upper() in ['F', 'FORCE']:
            self.char = char
            return
        if self and char != self.char:
            raise Exception(f'Word does not fit. Tried entering {char} on {self.char}')
        elif len(value) > 1:
            if dir.upper() in ['D', 'DN', 'DOWN']:
                if self.down == None:
                    raise Exception('Out of bounds')
                self.down.set(dir, value[1:])
                self.hasDown = True
            elif dir.upper() in ['A', 'ACROSS']:
                if self.across == None:
                    raise Exception('Out of bounds')
                self.across.set(dir, value[1:])
                self.hasAcross = True
        self.char = char


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

    # Return a list of all the words in the crossword with empty clues.
    def getWords(self):
        acrossCheck = []
        downCheck = []
        for i in range(self.size):
            acrossCheck.append([])
            downCheck.append([])
            for j in range(self.size):
                acrossCheck[i].append(False)
                downCheck[i].append(False)

        words = []
        number = 1
        for row in range(self.size):
            for col in range(self.size):
                if self[row][col]:
                    across = ''
                    down = ''
                    if not downCheck[row][col]:
                        i = row
                        while i < self.size and self[i][col]:
                            down += str(self[i][col])
                            downCheck[i][col] = True
                            i += 1
                    if not acrossCheck[row][col]:
                        j = col
                        while j < self.size and self[row][j]:
                            across += str(self[row][j])
                            acrossCheck[row][j] = True
                            j += 1

                    if len(across) > 1:
                        words.append(XClue(number, across, 'across'))
                    if len(down) > 1:
                        words.append(XClue(number, down, 'down'))
                    if len(across) + len(down) > 2:
                        number += 1
        return XCLues(words)

class XClue:
    def __init__(self, id: int, answer: str, dir: str, clue: str = ''):
        self.id = id
        if dir.upper() in ['D', 'DN', 'DOWN']:
            self.dir = 'Down'
        if dir.upper() in ['A', 'ACROSS']:
            self.dir = 'Across'
        self.answer = answer
        self.clue = clue

    def setClue(self, clue):
        self.clue = clue

    def __str__(self):
        return f'{self.id} {self.dir}: {self.clue} \n\t {self.answer}'

    def __lt__(self, other):
        if self.dir != other.dir and self.dir == 'Across':
            return True
        return self.id < other.id    
