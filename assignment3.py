# CMPUT 175 Assignment 3
# Author: Ian Morrison
# This program imports our AbacoStack and Card class, then plays a Towers of Hanoi-esque game. The player will input
# game dimensions, then the game will generate a random configuration card based on user input. The player must
# configure the game board such that all the letters match the configuration card.
from AbacoStack import Card, AbacoStack

def main():
    game = Game()
    game.play()

class Game():
    """
    This is our Game method. This initializes and runs our Abaco game by prompting the user for game board dimensions.
    While the game is not solved, the user will be continually prompted for input until the game is solved, or until
    the user quits
    """

    def __init__(self):
        self.solved = False
        self.continueGame = True


    def play(self):
        """
        This method actually plays the game by prompting the user for input, and coordinating what to do with said input
        :return: None
        """
        while self.continueGame:
            # While the user wants to continue playing, we remain in this loop.

            # This block of code creates starts a new set up of our game
            self.stacks, self.depth = self.setUp()
            self.card = Card(self.depth, self.stacks)
            beads = self.card.getBeads()
            self.abacoStack = AbacoStack(self.stacks, self.depth, beads)

            print('This is your configuration card. Manipulate the letters in the game stacks to match the card'
                  ' in as few moves as possible to win.')
            self.card.reset()
            self.card.show()
            print()
            self.abacoStack.show()

            while not self.solved:
                # This loop continues while the game is not solved
                self.getMove()

                displayCard = input('Would you like to show the configuration card and current moves? Y/N ')
                if displayCard.upper() == 'Y':
                    self.abacoStack.show(self.card.__str__())
                else:
                    self.abacoStack.show()

                if self.checkSolved():
                    again = input("Would you like to play again? Y/N")
                    if again.upper == 'Y':
                        self.play()
                    else:
                        self.solved = True
                        self.continueGame = False


    def checkSolved(self):
        """
        This method checks to see if the game board is solved
        :return: True if solved, False otherwise
        """
        return self.abacoStack.isSolved(self.card.__str__())

    def getMove(self):
        """
        This method gets our user input and validates it, then turns it into game functions by splitting multiple moves
        into individual ones. These are then passed into our validator. If the move is valid, we do it. Else, we finish
        the segment.
        :return:
        """
        valid = True
        moveList = []

        while valid:
            move = input("What would you like to do? ")
            move = move.replace(' ', '')

            if move.upper() == 'Q':
                self.solved = True
                self.continueGame = False

            if move.upper() == 'R':
                self.abacoStack.reset()
                valid = False

            elif len(move) > 10:
                # This reduces the user input into its maximum length if it exceeds it
                move = move[:10]
            chars = ''

            # This code block turns multiple moves into list items
            for i in range(len(move)):
                chars = chars + move[i]
                if i % 2 != 0:
                    moveList.append(chars)
                    chars = ''

            # This block goes through each possible move. If an invalid move occurs, we stop updating the board
            for move in moveList:
                if self.abacoStack.moveValidator(move) and valid == True:
                    self.abacoStack.moveBead(move)
                else:
                    valid = False
            valid = False

    def setUp(self):
        """
        This method sets up our game by getting user input for our stack count and depth
        :return:
        """
        valid = False

        while valid == False:
            try:
                stacks = int(input('How many stacks would you like to play with? '))
                depth = int(input("What depth would you like the game stacks? "))
                valid = True
            except Exception:
                print('Error. Please input integers.')

        return stacks, depth

main()