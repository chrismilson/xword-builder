import re

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
    def __init__(self, size: int = 0, filename: str = None):
        self.rows = []
        self.clues = []
        self.across = []
        self.down = []
        if filename != None:
            with open(filename) as f:
                s = f.read()
                across = re.search(r'ACROSS', s)
                down = re.search(r'DOWN', s)

                across = s[across.end():down.start()]
                down = s[down.end():]

                patt = re.compile(r'(\d+)\s+(\d+)\s+(\w+)(:)?(?(4)\s*([^\n]+))')

                across = patt.findall(across)
                down = patt.findall(down)

                for word in across:
                    size = max(size, int(word[1]) + len(word[2]) - 1)
                for word in down:
                    size = max(size, int(word[0]) + len(word[2]) - 1)
                self.size = size
                self.initCells()

                wordClues = {}

                for word in across:
                    self[int(word[0]) - 1][int(word[1]) - 1].set('A', word[2])
                    if word[3] == ':':
                        wordClues[word[2].upper()] = word[4]
                for word in down:
                    self[int(word[0]) - 1][int(word[1]) - 1].set('D', word[2])
                    if word[3] == ':':
                        wordClues[word[2].upper()] = word[4]
                self.getWords()
                for clue in self.clues:
                    try:
                        clue.setClue(wordClues[clue.answer], clues = self.clues)
                    except:
                        pass
        else:
            if size < 1:
                size = 1
            self.size = size
            self.initCells()

    def initCells(self):
        self.rows.append(XRow(self.size))
        for i in range(self.size - 1):
            self.rows.insert(0, XRow(self.size, self.rows[0]))

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

        acrossWords = []
        downWords = []
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
                        acrossWords.append(XClue(number, across, 'across'))
                    if len(down) > 1:
                        downWords.append(XClue(number, down, 'down'))
                    if len(across) > 1 or len(down) > 1:
                        number += 1

        acrossWords.sort()
        downWords.sort()
        words = acrossWords + downWords
        self.clues = words
        self.across = acrossWords
        self.down = downWords
        return words

class XClue:
    def __init__(self, id: int, answer: str, dir: str, clue: str = '', reveal: bool = False):
        self.id = id
        if dir.upper() in ['D', 'DN', 'DOWN']:
            self.dir = 'Down'
        if dir.upper() in ['A', 'ACROSS']:
            self.dir = 'Across'
        self.answer = answer
        self.clue = clue
        self.clues = None
        self.reveal = reveal

    def setClue(self, clue, clues = None):
        clue = re.sub(r'(.)\$\$(.)', self.dummy, clue)
        if clues:
            self.clues = clues
        clue = re.sub(r'\{(.*)\}', self.ref, clue)
        self.clue = clue

    def ref(self, matchobj):
        if self.clues != None:
            for clue in self.clues:
                if clue.answer.upper() == matchobj[1].upper():
                    return f'{clue.id} {clue.dir}'
        return matchobj[1]

    def dummy(self, matchobj):
        dummystring = ''
        if matchobj[1] == ' ':
            dummystring += '  '
        else:
            dummystring += matchobj[1]
        for i in self.answer:
            dummystring += '_ '
        if matchobj[2] == ' ':
            dummystring += ' '
        else:
            dummystring += matchobj[2]
        return dummystring

    def __str__(self):
        output = f'{self.id}\t{self.clue}'
        if not self.clue:
            output += self.answer
        if self.reveal:
            output += f'\n\t {self.answer}'
        return output

    def __lt__(self, other):
        if self.dir != other.dir and self.dir == 'Across':
            return True
        return self.id < other.id
