import copy

playerTypes = ['x', 'o']
openingsInRow = lambda a: [x for x in range(3) if isNone(a[x])]
isNone = lambda x: x is None
flipPlayer = lambda p: 'x' if p == 'o' else 'o'


def getDiagonals(rows):
    """Get a list of the diagonal rows, where rows is NxN matrix."""
    minimum = 0
    maximum = len(rows) - 1
    inc = lambda n: n + 1
    dec = lambda n: n - 1

    def diagonalHelper(startCol):
        change = inc if startCol == minimum else dec
        nextCol = startCol
        diagonal = []
        for row in rows:
            diagonal.append(row[nextCol])
            nextCol = change(nextCol)
        return diagonal

    return [diagonalHelper(minimum), diagonalHelper(maximum)]


def allSame(row):
    """Return row's cell's value if all cells the same, else False."""
    first = row[0]
    for i in row[1:]:
        if i != first:
            return False
    return True


def isWon(gameState):
    """Return an x or an o if that player won, else false."""
    getCol = lambda n: [x[n] for x in gameState]

    def checker(arr):
        if not all(arr):
            # Triggered if there is a None in the arr
            return False
        elif allSame(arr):
            return arr[0].lower()
        else:
            return False
    rows = gameState
    cols = [getCol(i) for i in range(3)]
    diagonals = getDiagonals(gameState)
    together = rows + cols + diagonals
    answers = [checker(x) for x in together]
    for a in answers:
        if a:
            return a
    return False


def evalGameResult(winnerType, playerType):
    otherPlayerType = 'x' if playerType == 'o' else 'x'
    if winnerType == playerType:
        return 100
    elif winnerType == otherPlayerType:
        return -100
    else:
        return 0


def allOpenSlots(gameState):
    """
    Get an array of tuples representing the open slots in the game.

    Assumes a 3x3 matrix. Returns a list of tuples representing the zero-
    indexed coordinates of open slots.
    """
    allOpenings = []
    for i in range(3):
        openings = openingsInRow(gameState[i])
        for opening in openings:
            allOpenings.append((i, opening))
    return allOpenings


def nextAvailableMove(gameState):
    """
    Get the next empty slot in the tic tac toe board.

    Assumes a 3x3 matrix. Returns a tuple (row, col), which is zero indexed.
    """
    for i in range(3):
        openings = openingsInRow(gameState[i])
        if len(openings) != 0:
            return (i, openings[0])


def makeMove(gameState, move, playerType):
    """Return a gamestate if the player makes the specified move."""
    row, col = move
    if not isNone(gameState[row][col]):
        raise ValueError
    newGameState = copy.deepcopy(gameState)
    newGameState[row][col] = playerType
    return newGameState


def minmax(gameState, playerType):
    """Gets the best move for a player in the form (row, col)."""
    def minmaxIter(gameState, playerTurn, depth=0):
        # Base conditions: Either there's a winner, or there's no next available
        # move
        # Check for winner
        winner = isWon(gameState)
        compareFn = max if playerType == playerTurn else min
        if winner:
            # Game over, evaluate game result
            endResult = evalGameResult(winner, playerType)
            return {'endResult': endResult, 'depth': depth}
        # Check for tie
        availableMoves = allOpenSlots(gameState)
        if len(availableMoves) < 1:
            return {'endResult': 0, 'depth': depth}

        moveHelper = lambda m: makeMove(gameState, m, playerTurn)
        mmHelper = lambda mv: minmaxIter(
            moveHelper(mv), flipPlayer(playerTurn), depth + 1
        )
        scoresWithDepth = [mmHelper(m) for m in availableMoves]
        scoresWODepth = [x['endResult'] for x in scoresWithDepth]
        return {'depth': depth, 'endResult': sum(scoresWODepth)}

    # Recurse
    possibleNextMoves = allOpenSlots(gameState)
    makeMoveHelper = lambda x: makeMove(gameState, x, playerType)
    seedBoard = {m: makeMoveHelper(m) for m in possibleNextMoves}
    moves = {k: minmaxIter(v, playerType) for k, v in seedBoard.items()}
    maxMoveValue = max([v['endResult'] for v in moves.values()])
    minDepth = min([v['depth'] for v in moves.values()])
    bestMoves = [
        k for k, v in moves.items() if v['endResult'] == maxMoveValue
    ]
    import pdb; pdb.set_trace()
    return bestMoves[0]
