import math
import copy

class C2dBoard:
    _board = []

    _depthSearchIdx = 0
    _boardDimensions = 9  # Gives us the NxN board
    _boxOffsetValues = 0  # Used to get the nxn box
    _solvedPoints = _boardDimensions ** 2  # This is how many values must be on the board to be solved.

    _rowTitles = 'ABCDEFGHI'
    INIT_CELL_VALUE = '123456789'


    def __init__(self):
        for index in range(self._boardDimensions):
            theRow = [self.INIT_CELL_VALUE] * self._boardDimensions
            self._board.append(theRow)

        # Get the dimensions of each box. nxn
        self._boxOffsetValues = int(math.sqrt(self._boardDimensions))


    @property
    def boardToDictionary(self):
        iVarRow = 0;
        iVarCol = 0;

        dictionaryBoard = {}

        for rowIndex in range(self._boardDimensions):
            for colIndex in range(self._boardDimensions):
                key = self.characterForRowNumber(rowIndex) + str(colIndex + 1)
                dictionaryBoard[key] = self._board[rowIndex][colIndex]

        return dictionaryBoard


    @property
    def isSolved(self):
        solvedStat = True

        for rowIdx in range(self._boardDimensions):
            for colIdx in range(self._boardDimensions):
                if (len(self._board[rowIdx][colIdx]) > 1):
                    solvedStat = False
                    break

        return solvedStat


    def solveSudoku(self):
        for bxIdx in range(self._boardDimensions):
            for idx in range(self._boardDimensions):
                self.clearBox(idx)

            self.determinOnlyPossibleChoiceInBox(bxIdx)
            self.resolveGhostPairings(0, True) #Test the columns for ghost pairs
            self.resolveGhostPairings(0, False) #Test the rows for ghost pairs

            if (self.isSolved == True):
                return

        if self.isSolved == True:
            return

        #--TEST
        self.displayBoard()
        print("\n****************\n")
        #--END TEST

        sortedCellsArray = self.sortCellsForDepthFirst()
        self.performReplacementForDepthFirst(sortedCellsArray, self._depthSearchIdx)

        #--TEST
        print(len(sortedCellsArray))
        print(sortedCellsArray)
        print("\n****************\n")
        #self.performReplacementForDepthFirst()
        #--END TEST



    # getBoxGrid:
    # Pre:The grid/board is allocated
    # Post:The point/tuple is returned
    # The sequence is breath first. ie: (0, 0) -> (0, 3) -> (0, 6) -> ... -> (0, (DIM - SQRT(DIM)) would be the top row
    #                                  (1, 0) -> (1, 3) -> (1, 6) -> ... -> (1, (DIM - SQRT(DIM)) would be the 2nd row
    # In a 3x3 example: [Boxes are 0th index based]
    # Parameter: 0 = (0, 0), 1 = (0, 3), 2 = (0, 6)
    # Parameter: 3 = (1, 0)
    # Parameter: 7 = (2, 3)
    def getBoxGrid(self, boxIndex):
        if (boxIndex < 0) or (boxIndex >= self._boardDimensions):
            return None

        rowIndex = int(boxIndex / self._boxOffsetValues) * self._boxOffsetValues
        colIndex = (int(boxIndex % self._boxOffsetValues)) * self._boxOffsetValues

        return (rowIndex, colIndex)


    def clearBox(self, boxIndex):
        point = self.getBoxGrid(boxIndex)

        rowIndex = point[0]
        colIndex = point[1]

        relevantChangesMade = False

        for _ in range(self._boxOffsetValues):  # Iterate the rows
            for _ in range(self._boxOffsetValues):  # Iterate the columns

                if len(self._board[rowIndex][colIndex]) == 1:  # Be sure we can determine useful information
                    relevantChangesMade = self.clearBoxOfValue(point, self._board[rowIndex][colIndex])

                colIndex += 1

            rowIndex += 1
            colIndex = point[1]

            if relevantChangesMade == True:
                relevantChangesMade = False
                self.clearBox(boxIndex)


    def clearBoxOfValue(self, boxIndexPoint, numValue):
        hasRelevantChanges = False

        rowIdx = boxIndexPoint[0]
        colIdx = boxIndexPoint[1]

        for _ in range(self._boxOffsetValues):
            for _ in range(self._boxOffsetValues):

                if (len(self._board[rowIdx][colIdx]) > 1) and (numValue in self._board[rowIdx][colIdx]):
                    self._board[rowIdx][colIdx] = self._board[rowIdx][colIdx].replace(numValue, "")
                    if (hasRelevantChanges == False) and (len(self._board[rowIdx][colIdx]) == 1):
                        hasRelevantChanges = True  # You only have relevent changes when a square drops to len 1

                if len(self._board[rowIdx][colIdx]) == 1:  # Either it was already a solved square or just became solved
                    self.clearRowsAndColumnsOfValue(rowIdx, colIdx, self._board[rowIdx][colIdx])

                colIdx += 1

            rowIdx += 1
            colIdx = boxIndexPoint[1]

        return hasRelevantChanges


    def clearRowsAndColumnsOfValue(self, rowIdx, colIdx, numValue):
        self.clearRowOfValue(rowIdx, numValue)
        self.clearColOfValue(colIdx, numValue)


    def clearRowOfValue(self, rowIdx, numValue):
        if (numValue == None) or (len(numValue) == 0):
            return

        droppedToOneOption = ''  # As info is added, it may become something like '123456789'

        for colIdx in range(self._boardDimensions):  # 0 to N number of columns
            if (numValue in self._board[rowIdx][colIdx]) and (len(self._board[rowIdx][colIdx]) > 1):
                self._board[rowIdx][colIdx] = self._board[rowIdx][colIdx].replace(numValue, "")

                if (len(self._board[rowIdx][colIdx]) == 1):
                    droppedToOneOption += self._board[rowIdx][colIdx]

        for num in droppedToOneOption:
            self.clearRowOfValue(rowIdx, num)


    def clearColOfValue(self, colIdx, numValue):
        if (numValue == None) or (len(numValue) == 0):
            return

        droppedToOneOption = ''  # As info is added, it may become something like '123456789'

        for rowIdx in range(self._boardDimensions):
            if (numValue in self._board[rowIdx][colIdx]) and (len(self._board[rowIdx][colIdx]) > 1):
                self._board[rowIdx][colIdx] = self._board[rowIdx][colIdx].replace(numValue, "")

                if (len(self._board[rowIdx][colIdx]) == 1):
                    droppedToOneOption += self._board[rowIdx][colIdx]

        for num in droppedToOneOption:
            self.clearColOfValue(colIdx, num)


    def setGridValues(self, solutionString):
        if (len(solutionString) != self._boardDimensions ** 2):
            return None

        rowIndex = -1;
        for index in range(self._boardDimensions ** 2):
            cellValue = solutionString[index]

            if ((index % self._boardDimensions) == 0):
                rowIndex += 1

            colIndex = index % self._boardDimensions

            if (cellValue != '.'):
                self._board[rowIndex][colIndex] = cellValue


    # Parameter 'colRowSearch' true = Clear via columun. ie: (0, 0), (0, 1), (0, 2)...
    # Parameter 'colRowSearch' false = Clear via row. ie: (0, 0), (1, 0), (2, 0)...
    def resolveGhostPairings(self, Idx, colRowSearch):
        if (Idx < 0) or (Idx >= self._boardDimensions):
            return

        rowIdx = 0
        colIdx = 0

        if colRowSearch == True:
            colIdx = Idx
        else:
            rowIdx = Idx

        ghosts = []

        for runningIdx in range(self._boardDimensions):

            if colRowSearch == True:
                rowIdx = runningIdx
            else:
                colIdx = runningIdx

            cellGhostInfo = self._board[rowIdx][colIdx]

            if (len(cellGhostInfo) != 2):
                continue

            if (cellGhostInfo in ghosts):#Test if we now have a ghost pair
                self.clearGhostPairBy(cellGhostInfo, Idx, colRowSearch)
                ghosts.remove(cellGhostInfo)
            else:
                ghosts.append(cellGhostInfo)

        if self.isSolved == False:
            self.resolveGhostPairings(Idx + 1, colRowSearch)


    # Parameter 'colRow' true = Clear via columun. ie: (0, 0), (0, 1), (0, 2)...
    # Parameter 'colRow' false = Clear via row. ie: (0, 0), (1, 0), (2, 0)...
    def clearGhostPairBy(self, ghostPairValue, idx, colRow):
        rowIdx = 0
        colIdx = 0;

        if(colRow == True):
            colIdx = idx
        else:
            rowIdx = idx

        for _ in range(self._boardDimensions):
            if (len(self._board[rowIdx][colIdx]) > 2) and (ghostPairValue in self._board[rowIdx][colIdx]):
                self._board[rowIdx][colIdx] = self._board[rowIdx][colIdx].replace(ghostPairValue, "")

            if(colRow == True):
                rowIdx += 1 #Means our column index does not change
            else:
                colIdx += 1 #Means our row index does not change


    # Think of the cells in the box as a grid of letters
    #
    # A B C
    # D E F
    # G H I
    #
    def determinOnlyPossibleChoiceInBox(self, boxID):
        boxValues = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

        boxOptionValues = {'A': '', 'B': '', 'C': '', 'D': '', 'E': '', 'F': '', 'G': '', 'H': '', 'I': ''}

        boxPoint = self.getBoxGrid(boxID)

        boxIdx = -1
        rowIndex = boxPoint[0]
        colIndex = boxPoint[1]

        # We need to iterate over all the cells in the box of 9 values
        for _ in range(self._boxOffsetValues):
            for _ in range(self._boxOffsetValues):
                boxIdx += 1

                # if The value in the cell has more than 1 possibility - record the options
                if (len(self._board[rowIndex][colIndex]) > 1):
                    key = self.characterForRowNumber(boxIdx)  # Gets us an 'A', 'B', etc for our container to test later
                    boxOptionValues[key] = self._board[rowIndex][colIndex]

                    # A value in the cell of '2467' will mean we iterate 4 times and we'll increment the
                    # number of time 2 - 4 - 6 - 7 appear in the box. We're looking for values that only
                    # appear once.
                    for strIdx in range(len(self._board[rowIndex][colIndex])):
                        numVal = self._board[rowIndex][colIndex][strIdx]
                        boxValues[numVal] += 1

                colIndex += 1

            rowIndex += 1
            colIndex = boxPoint[1]

        # Now we iterate over the array that holds the numbers in the block and the number of times each occurs.
        # NOTE: Any cell which already has a single number (ie: It's solved is not included).
        for uniqeIdx in boxValues:
            if (boxValues[str(uniqeIdx)] == 1):  # If the value only occures once
                for optIndx in boxOptionValues:  # Find the cell that includes the numeric value that only occurs once
                    valKey = boxOptionValues[optIndx]
                    if (str(uniqeIdx) in boxOptionValues[optIndx]):
                        boxCellPt = self.getRelativeBoxOffset(boxID, optIndx)
                        self._board[boxCellPt[0]][boxCellPt[1]] = str(uniqeIdx)


    # Any cell not solved will be a .
    def boardToString(self):
        boardStr = ''

        # Row first
        for rowIdx in range(self._boardDimensions):
            for colIdx in range(self._boardDimensions):
                if (len(self._board[rowIdx][colIdx]) == 1):
                    boardStr += self._board[rowIdx][colIdx]
                else:
                    boardStr += '.'

        return boardStr


    def displayBoard(self):
        cols = '123456789'

        values = self.boardToDictionary

        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """

        width = 0
        for rowIndex in range(self._boardDimensions):
            for colIndex in range(self._boardDimensions):
                currWidth = self.optionsRemainingAtCell(rowIndex, colIndex)
                if (currWidth > width):
                    width = currWidth

        width += 1
        line = '+'.join(['-' * (width * 3)] * 3)

        for r in self._rowTitles:
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in cols))

            if r in 'CF':
                print(line)
        return


    def getRelativeBoxOffset(self, boxIdx, cellID):
        point = self.getBoxGrid(boxIdx)

        rowIdx = 0
        colIdx = 1

        rowPt = point[0]
        colPt = point[1]

        # if cellID == 'A':
        #    return (rowPt, colPt)
        if cellID == 'B':
            colPt = point[colIdx] + 1
        elif cellID == 'C':
            colPt = point[colIdx] + 2
        elif cellID == 'D':
            rowPt = point[rowIdx] + 1
        elif cellID == 'E':
            rowPt = point[rowIdx] + 1
            colPt = point[colIdx] + 1
        elif cellID == 'F':
            rowPt = point[rowIdx] + 1
            colPt = point[colIdx] + 2
        elif cellID == 'G':
            rowPt = point[rowIdx] + 2
        elif cellID == 'H':
            rowPt = point[rowIdx] + 2
            colPt = point[colIdx] + 1
        elif cellID == 'I':
            rowPt = point[rowIdx] + 2
            colPt = point[colIdx] + 2

        return (rowPt, colPt)


    def optionsRemainingAtCell(self, row, col):
        if (row < 0) or (row >= self._boardDimensions) or (col < 0) or (col >= self._boardDimensions):
            return 0

        return len(self._board[row][col])


    def rowCharacterToNumber(self, charRow):
        if (charRow == 'A'):
            return 0
        elif (charRow == 'B'):
            return 1
        elif (charRow == 'C'):
            return 2
        elif (charRow == 'D'):
            return 3
        elif (charRow == 'E'):
            return 4
        elif (charRow == 'F'):
            return 5
        elif (charRow == 'G'):
            return 6
        elif (charRow == 'H'):
            return 7
        elif (charRow == 'I'):
            return 8
        else:
            return 0


    def characterForRowNumber(self, charRow):
        if (charRow == 0):
            return 'A'
        elif (charRow == 1):
            return 'B'
        elif (charRow == 2):
            return 'C'
        elif (charRow == 3):
            return 'D'
        elif (charRow == 4):
            return 'E'
        elif (charRow == 5):
            return 'F'
        elif (charRow == 6):
            return 'G'
        elif (charRow == 7):
            return 'H'
        elif (charRow == 8):
            return 'I'
        else:
            return 'A'

    #Depth-first code

    def sortCellsForDepthFirst(self):
        cellToGuess = []

        for rowIdx in range(self._boardDimensions):
            for colIdx in range(self._boardDimensions):

                cellInfo = self._board[rowIdx][colIdx]
                lenOfCellData = len(cellInfo)
                cellIdx = (rowIdx, colIdx, cellInfo)

                if lenOfCellData == 1:
                    continue #Any cell with a single option is solved
                elif lenOfCellData == 2:
                    cellToGuess.insert(0, cellIdx) #Any cell with two options automatically is the shortest possible
                    continue
                elif len(cellToGuess) == 0:
                    cellToGuess.append(cellIdx)
                    continue

                wasInserted = False
                for idx in range(len(cellToGuess)):
                    point = cellToGuess[idx]

                    cellRow = point[0]
                    cellCol = point[1]

                    if(len(self._board[cellRow][cellCol]) < lenOfCellData):
                        continue;
                    else:
                        wasInserted = True
                        cellToGuess.insert(idx, cellIdx)
                        break

                if wasInserted == False:
                    cellToGuess.append(cellIdx)


        return cellToGuess

    #Param: replacmentIndices - This is the array indice of 0 - N when N is the
    #      number of tuples in the options array. The reason this is like this
    #      is because we'll need two indicies. 1 for the tuple's index in the
    #      array and another for the testing value. ie: If we're testing replacing
    #      a cell [at array indice 12] which has the value "2478" and we want to
    #      test if replacing the cell with 7 will work, we'll need separate indexs of:
    #      12 and 2. 12 for the array and 2 for the string's character index.
    def performReplacementForDepthFirst(self, arrOptions, arrayTupleIndice):
        if(arrayTupleIndice >= len(arrOptions)):
            return

        tmpBoard = self._board #Just for easier referencing

        tpl = arrOptions[arrayTupleIndice]



        self._depthSearchIdx += 1

































