import sys
import os
import random
import time
import copy
import re

import computer_moves


playerTypes = ['x', 'o']
wrongInputMessage = (
    'I do not understand. ' +
    'To make a move, type the character for the row, then the number for ' +
    'the Row. For example, "A 2". Type "q" to quit.'
)
isTied = lambda g: len(computer_moves.allOpenSlots(g)) < 1
welcome_message = (
    "Welcome to tic-tac-toe. To make a move, type in the  " +
    "row and column numbers. For instance, to select the " +
    "second column on the first row, type 2 1\n" +
    "To quit, type q.\n"
)


def cleanInput(i):
    """Turn human input into a move our game object can understand."""
    toNum = lambda n: {"A": 1, "B": 2, "C": 3}[n]
    cleanedArr = re.sub(r'\s+', '', i)
    if len(cleanedArr) != 2:
        raise ValueError()
    elif cleanedArr[0].lower() not in ['a', 'b', 'c']:
        raise ValueError()
    elif int(cleanedArr[1]) not in [1, 2, 3]:
        raise ValueError()
    else:
        return {
            'column': toNum(cleanedArr[0]),
            'row': int(cleanedArr[1])  # For zero-indexing
        }


def clearScreen():
    """Clear screen using correct command for os."""
    os.system('cls' if os.name == 'nt' else 'clear')


def drawBoard(boardState):
    """Get a list of strings that when printed shows the tic tac toe board."""
    headerRow = "     A   B   C\n"
    breakLine = "   +---+---+---+"
    lines = [headerRow, breakLine]

    def colVals(n):
        """Helper function to format board values for display."""
        rawValues = [boardState[n - 1][i] for i in range(3)]
        # Need to replace None values with spaces
        replaceNones = lambda x: x if x is not None else ' '
        displayVals = [replaceNones(x) for x in rawValues]
        return displayVals

    for n in range(1, 4):
        line = '{}  | {} | {} | {} |'.format(n, *colVals(n))
        lines.append(line)
        lines.append(breakLine)
    return lines


def drawScreen(messages, game, print=print):
    """Draw the tic tac toe board, any messages and the prompt."""
    clearScreen()
    if game:
        [print(ln) for ln in drawBoard(game.state())]
        print(' ' * 5)
    if messages:
        for message in messages:
            print(message)


def handleMove(coordinates, game, playerType, message_queue):
    """A wrapper for the makeMove method."""
    try:
        game.makeMove(
            coordinates['row'],
            coordinates['column'],
            playerType
        )
    except ValueError:
        message_queue.append('You cannot make that move')
        return game


class GameState:
    """A class to represent the state of our game and handle changes."""

    def __init__(self, humanPlayer, nextMove='x'):
        assert humanPlayer.lower() in playerTypes
        self.human = humanPlayer.lower()
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
        # Zero index rows and cols
        rowAdjusted, colAdjusted = row - 1, col - 1
        if self.rows[rowAdjusted][colAdjusted] or row > 3 or col > 3:
            raise ValueError
        self.rows[rowAdjusted][colAdjusted] = playerType
        self.toggleNextMove()
        return self


def runGame(game, message_queue=[]):
    """Main game loop."""
    while True:
        # Check if game is done
        if isTied(game.state()):
            message_queue = ['Tied! Game over!']
            drawScreen(message_queue, game)
            time.sleep(5)
            break
        elif computer_moves.isWon(game.state()):
            winner = computer_moves.isWon(game.state())
            message_queue = ['Game over! {} Won!'.format(winner.upper())]
            drawScreen(message_queue, game)
            time.sleep(5)
            break
        # Start gameplay
        drawScreen(message_queue, game)
        message_queue = []
        # Handle human move, if it is their turn
        if game.human == game.nextMove:
            uinput = input('You are player %s\n' % game.human +
                            'Make your move: ')
            if 'q' in uinput.lower():
                print('Thanks for playing!')
                sys.exit()
            try:
                moveCoordinates = cleanInput(uinput)
            # Check for bad user input
            except ValueError:
                message_queue.append(wrongInputMessage)
                continue
            handleMove(moveCoordinates, game, game.human, message_queue)
        # Handle computer move, if it's computer's turn
        else:
            moveCoords = computer_moves.minmax(game.state(), game.nextMove)
            moveCoords = {
                'row': moveCoords[0] + 1,
                'column': moveCoords[1] + 1
            }
            message_queue.append('Computer moved to %s' % moveCoords)
            handleMove(moveCoords, game, game.nextMove, message_queue)
            continue


if __name__ == '__main__':
    clearScreen()
    # Player selects X or O
    while True:
        uinput = input('Which player do you want to be? X or O?\n-> ')
        if uinput.lower() in playerTypes:
            break
        else:
            clearScreen()
            print('You need to type "X" or "O" to select a player')
    # Initialize and start game
    game = GameState(humanPlayer=uinput.lower())
    message_queue = ["X goes first".format(uinput.upper())]
    runGame(game, message_queue)
