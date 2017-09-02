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
    """Return an x or an o if that player won, else False."""
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


def evalGameResult(winnerType, playerType, depth):
    if winnerType == playerType:
        return 100 - depth
    else:
        return depth -100


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
    """Gets the best move for a player in the form (row, col) not 0 indexed."""
    bestMove = None

    def minmaxIter(gameState, playerTurn, depth=0):
        # Base conditions: Either there's a winner, or there's no next
        # available move
        # Check for winner
        winner = isWon(gameState)
        compareFn = max if playerType == playerTurn else min
        if winner:
            # Game over, evaluate game result
            endResult = evalGameResult(winner, playerType, depth)
            return endResult
        # Check for tie
        availableMoves = allOpenSlots(gameState)
        if len(availableMoves) < 1:
            return 0

        # Nothing? Recurse
        scores = []
        moves = []
        mvHelper = lambda m: makeMove(gameState, m, playerTurn)
        for mv in availableMoves:
            moves.append(mv)
            scores.append(minmaxIter(
                mvHelper(mv),
                flipPlayer(playerTurn),
                depth + 1
            ))
        highestOrLowest = compareFn(scores)
        if depth == 0:
            moveIndex = scores.index(highestOrLowest)
            # Set bestMove
            nonlocal bestMove
            bestMove = moves[moveIndex]
        return highestOrLowest

    # Recurse
    result = minmaxIter(gameState, playerType)
    return bestMove
