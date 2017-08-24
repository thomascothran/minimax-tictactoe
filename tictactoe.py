import sys
import os
import random
import copy

import computer_moves


playerTypes = ['x', 'o']
wrongInputMessage = ('I do not understand. ' +
                     'To make a move, type the number of the row, then the ' +
                     'column. For example, "1 2". Type "q" to quit.')


def welcome_message(playerType):
    if playerType not in playerTypes:
        raise ValueError
    return (
        "Welcome to tic-tac-toe. To make a move, type in the  " +
        "row and column numbers. For instance, to select the " +
        "second column on the first row, type 2 1 \n" +
        "To quit, type q. \n You are player {}".format(playerType)
    )


def cleanInput(i):
    cleanedArr = [int(x) for x in i if x in ['1', '2', '3']]
    if len(cleanedArr) != 2:
        raise ValueError()
    else:
        return {'row': cleanedArr[0], 'column': cleanedArr[1]}


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def drawScreen(messages, game, print=print):
    clearScreen()
    if game:
        print(game.draw())
        print(' ' * 5)
    if messages:
        for message in messages:
            print(message)


def handleMove(coordinates, game, playerType, message_queue):
    try:
        game.makeMove(
            coordinates['row'],
            coordinates['column'],
            playerType
        )
    except ValueError:
        message_queue.append('You cannot make that move')
        return game


def computerMove(game):
    return game.makeMove(3, 3, game.computerPlayer)


class GameState:
    """A class to represent the state of our game and handle changes."""

    def __init__(self, nextMove='x'):
        self.human = random.choice(playerTypes)
        self.computerPlayer = 'x' if self.human != 'x' else 'o'
        self.nextMove = nextMove
        self.rows = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]

    def state(self):
        gameState = copy.deepcopy(self.rows)
        return gameState

    def toggleNextMove(self):
        self.nextMove = 'x' if self.nextMove != 'x' else 'o'
        return self

    def makeMove(self, row, col, playerType):
        if self.rows[row - 1][col - 1] or row > 3 or col > 3:
            raise ValueError

        self.rows[row - 1][col - 1] = playerType
        self.toggleNextMove()
        return self

    def draw(self):
        formatRow = lambda r: "+ {} {} {} +".format(*r)
        repNones = lambda sArr: [' ' if not s else s for s in sArr]
        rowArr = [formatRow(repNones(r)) for r in self.rows]
        table = '\n'.join(rowArr)
        return table


if __name__ == '__main__':
    game = GameState()
    message_queue = [welcome_message(game.human)]
    while True:
        drawScreen(message_queue, game)
        message_queue = []
        if game.human == game.nextMove:
            uinput = input('You are player %s\n' % game.human +
                            'Make your move: ')
            if 'q' in uinput.lower():
                print('Thanks for playing!')
                sys.exit()
            try:
                moveCoordinates = cleanInput(uinput)
            except ValueError:
                message_queue.append(wrongInputMessage)
                continue
            handleMove(moveCoordinates, game, game.human, message_queue)
        else:
            moveCoords = computer_moves.minmax(game.state(), game.nextMove)
            moveCoords = {'row': moveCoords[0] + 1, 'column': moveCoords[1] + 1}
            message_queue.append('Computer moved to %s' % moveCoords)
            handleMove(moveCoords, game, game.nextMove, message_queue)
            continue
