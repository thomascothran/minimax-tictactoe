import computer_moves
from pprint import pprint

crossX = [['x', None, 'o'], [None, 'x', None], ['o', None, 'x']]
easyWin = [['x', None, 'o'], [None, None, 'o'], ['o', None, 'x']]
horizonalO = [['o', 'o', 'o'], [None, 'x', 'x'], ['x', 'x', None]]
allNone = [[None, None, None], [None, None, None]]
oGoingToWin = [['o', 'x', 'x'], ['x', None, None], [None, None, 'o']]
noWinners = [['x', 'o', 'x'], ['o', 'x', 'o'], ['x', 'x', 'o']]
weirdCase = [['x', 'x', 'o'], [None, 'o', None], [None, None, None]]

"""
print(computer_moves.isWon(crossX))
print(computer_moves.isWon(horizonalO))
print(computer_moves.isWon(allNone))
print(str(computer_moves.nextAvailableMove(allNone)) + ' should be (0, 0)')
print(str(computer_moves.nextAvailableMove(horizonalO)) + ' should be (1, 0)')
print(str(computer_moves.allOpenSlots(noWinners)) + ' should be []')
print(str(computer_moves.allOpenSlots(horizonalO)) +
      ' should be [(1, 0), (2, 2)]')
print(
    str(computer_moves.nextBestMove(noWinners, 'x')) +
    ' should be 0'
)
print(
    str(computer_moves.nextBestMove(crossX, 'x')) +
    ' should be 100'
)
print(
    str(computer_moves.nextBestMove(crossX, '0')) +
    ' should be -100'
)
print(
    str(computer_moves.makeMove(allNone, (0, 0), 'x')[0]) +
    ' should be ["x", None, None]'
)
pprint(str(computer_moves.minmax(easyWin, 'o')))
pprint(str(computer_moves.minmax(oGoingToWin, 'o')))
"""
assert computer_moves.flipPlayer('x') == 'o'
assert computer_moves.minmax(weirdCase, 'x') == (2, 0)
print(str(computer_moves.minmax(weirdCase, 'x')))
