class CSudoku:
    BOARD_DIMENSION_N = 9 #We can use this for X & Y since we're guaranteed NxN board
    COMPLETED_BOARD_VALUES_LEN = BOARD_DIMENSION_N**2

    _boardRow = None
    _sudokuBoard = {}# {'H', '[0...(N-1)]'}
    _boxPlaceHolder = None
    _rowIndices = []

    def __init__(self):
        _boxPlaceHolder = '.'
        _boardRow = None
        _rowIndices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    def constructBoard(self, row = 0, useTestIndicies=True):
        if(row >= self.BOARD_DIMENSION_N):
            return

        rowCharIndex = self.getRowChar(row)

        testIndicyVal = 5;
        rowIndicies = []
        for index in range(self.BOARD_DIMENSION_N):
            if(useTestIndicies == False) :
                rowIndicies.append('.')
            else:
                if(index == testIndicyVal):
                    rowIndicies.append(str(index + 1))
                else:
                    rowIndicies.append('.')

        self._sudokuBoard[rowCharIndex] = rowIndicies

        row += 1
        self.constructBoard(row)

    def getAllRowsInColumn(self, colum):
        rowsData = {}

        for rowIndex in range(self.BOARD_DIMENSION_N):
            rowKeyChar = self.getRowChar(rowIndex)

            rowVal = self._sudokuBoard[rowKeyChar];#All the values on a single row
            rowFilledValue = rowVal[rowIndex]
            rowsData[rowKeyChar] = rowFilledValue

        return  rowsData;

    def getRowChar(self, currentRow):
        if(currentRow == 0):
            return 'A'
        elif(currentRow == 1):
            return 'B'
        elif(currentRow == 2):
            return 'C'
        elif(currentRow == 3):
            return 'D'
        elif(currentRow == 4):
            return 'E'
        elif(currentRow == 5):
            return 'F'
        elif(currentRow == 6):
            return 'G'
        elif(currentRow == 7):
            return 'H'
        elif(currentRow == 8):
            return 'I'


sudoku = CSudoku()
sudoku.constructBoard()
print(sudoku._sudokuBoard)
print(sudoku.getAllRowsInColumn(3))


"""
board = CSudokuBoard();

#print(board._boxes)
#print(board._rowUnits)
#print(board._colUnits)
#print(board._squareUnits)
#print(board._unitList)

boardVals = board.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
print(boardVals)
board.displayBoard(boardVals)
#print(board.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))
"""