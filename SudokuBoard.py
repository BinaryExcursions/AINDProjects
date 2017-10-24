class CSudokuBoard:
    _rows = 'ABCDEFGHI'
    _cols = '123456789'

    BOARD_DIM = 9
    _boxes = None
    _rowUnits = None
    _colUnits = None
    _squareUnits = None #This is the 2D list of the boxex. 0th index of each list is the next box
    _unitList = None
    _theBoard = {}

    def __init__(self):
        self._boxes = self.cross(self._rows, self._cols)
        self._rowUnits = [self.cross(r, self._cols) for r in self._rows]
        self._colUnits = [self.cross(self._rows, c) for c in self._cols]
        self._squareUnits = [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

        self._unitList = self._rowUnits + self._colUnits + self._squareUnits

    def cross(self, a, b):
        return [s + t for s in a for t in b]

    def eliminate(self, board):
        self.eliminateViaBox(board)


    def displayBoard(self, values):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(values[s]) for s in self._boxes)

        line = '+'.join(['-' * (width * 3)] * 3)

        for r in self._rows:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self._cols))
            if r in 'CF':
                print(line)
        return


    def grid_values(self, solutionString):
        if (len(solutionString) != self.BOARD_DIM ** 2):
            return None

        self._theBoard = {}  # Clear out the board
        for index in range(self.BOARD_DIM ** 2):
            pairVal = solutionString[index]

            if (pairVal == '.'):
                self._theBoard[self._boxes[index]] = '123456789'
            else:
                self._theBoard[self._boxes[index]] = solutionString[index]

        return self._theBoard


    def eliminateViaBox(self, board):
        for boxIndex in range(self.BOARD_DIM):
            currBox = self._squareUnits[boxIndex]

            for key in currBox:
                if(len(self._theBoard[key]) != 1) :
                    continue

                rowIndex = key[0]
                colIndex = int(key[1]) -1

                self.removeValueOptionFromEntireBox(currBox, self._theBoard[key])

                #Our Row index is a letter: 'A' - 'I'
                self.removeValueOptionFromEntireRow(rowIndex, self._theBoard[key])
                self.removeValueOptionFromEntireCol(colIndex, self._theBoard[key])


    def removeValueOptionFromEntireBox(self, theBox, numValue):
        for key in theBox:
            if(len(self._theBoard[key]) <= 1):
                continue

            self._theBoard[key] = self._theBoard[key].replace(numValue, "")


    def removeValueOptionFromEntireRow(self, rowIndex, numValue):
        for index in range(self.BOARD_DIM):
            dictKey = rowIndex + str(index + 1)
            if(len(self._theBoard[dictKey]) > 1) :
                self._theBoard[dictKey] = self._theBoard[dictKey].replace(numValue, "")


    #ColIndex comes in as a 0th index value
    def removeValueOptionFromEntireCol(self, colIndex, numValue):
        for index in range(self.BOARD_DIM):
            dictKey = self.characterForRowNumber(index) + str(colIndex + 1)
            if (len(self._theBoard[dictKey]) > 1):
                self._theBoard[dictKey] = self._theBoard[dictKey].replace(numValue, "")


    def characterForRowNumber(self, charRow):
        if(charRow == 0):
            return 'A'
        elif(charRow == 1):
            return 'B'
        elif(charRow == 2):
            return 'C'
        elif(charRow == 3):
            return 'D'
        elif(charRow == 4):
            return 'E'
        elif(charRow == 5):
            return 'F'
        elif(charRow == 6):
            return 'G'
        elif(charRow == 7):
            return 'H'
        elif(charRow == 8):
            return 'I'
        else:
            return 'A'
