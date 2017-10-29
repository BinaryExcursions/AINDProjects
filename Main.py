from SudokuBoard import CSudokuBoard
from TwoDimBoard import C2dBoard

"""
board = CSudokuBoard();

boardVals = board.grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
board.displayBoard(boardVals)

board.eliminate(boardVals)

print("\n*******\n")

board.displayBoard(boardVals)
"""

tdTest = C2dBoard();

#                   123456789012345678901234567890123456789012345678901234567890123456789012345678901
# tdTest.setGridValues('..3.216..9..345..1..18764....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
# tdTest.setGridValues('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')
tdTest.setGridValues('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
# tdTest.setGridValues ('4.....8.5.3..........7......2.....6.....8.4...4..1.......6.3.7.5.32.1...1.4......')


tdTest.solveSudoku()
tdTest.displayBoard()
print(tdTest.boardToString())
print(tdTest.isSolved)
