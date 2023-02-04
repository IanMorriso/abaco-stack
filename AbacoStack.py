# CMPUT 175 Assignment 3
# Author: Ian Morrison

import random

import string
def main():
    pass
class AbacoStack:
    def __init__(self, stacks, depth, beads):
        self.stackCount = stacks
        self.depth = depth
        self.topList = ['.' for i in range(stacks + 2)]
        self.stacks = []
        self.beads = beads
        self.beads.sort()
        self.moves = 0

        self.stackPopulate()

    def reset(self):
        """
        This method resets our game back to the starting point
        :return:
        """
        self.moves = 0
        self.stacks = []
        self.topList = ['.' for i in range(len(self.topList))]
        self.stackPopulate()

    def stackPopulate(self):
        """
        This method populates our stacks with beads such that it fulfills the user's parameters
        :return: None
        """
        beads = self.beads.copy()
        for color in range(self.stackCount):
            stack = BStack(self.depth)
            self.stacks.append(stack)
        for stack in range(self.stackCount -1, -1, -1):
            for i in range(self.depth):
                self.stacks[stack].push(beads.pop())


    def moveBead(self, move):
        """
        This method moves our beads around our stacks. Based on the direction and stack number provided, we move the
        beads around to the desired locations
        :param move:
        :return: None
        """
        empty = '.'
        stack = int(move[0])
        direction = move[1]

        if direction == 'd':
            self.stacks[stack-1].push(self.topList[stack])
            self.topList[stack] = empty
        if direction == 'u':
            color = self.stacks[stack - 1].pop()
            self.topList[stack] = color
        if direction == 'l':
            self.topList[stack - 1] = self.topList[stack]
            self.topList[stack] = empty
        if direction == 'r':
            self.topList[stack + 1] = self.topList[stack]
            self.topList[stack] = empty

        self.moves += 1

    def moveValidator(self, move):
        """
        This method checks if the proposed move is valid or not. It checks each possible invalid condition and raises an
        exception if one is found. If no exceptions are raised, the move must be valid.
        :param move:
        :return: None
        """
        #valid = False
        #while not valid:
        if move == 'Q' or move == 'R':
            return True
        else:
            try:
                assert len(move) == 2, 'Error. Your move must be 2 characters, or "Q" to quit, or "R" to reset.'
                stack = int(move[0])
                direction = move[1].lower()
                assert type(stack) is int, 'Error. The first character must be an integer of a valid stack.'
                assert direction in 'udlr', 'Error. The second character must be a valid move type. (u, d, l, or r).'
                if stack == 0 and direction != 'r':
                    raise Exception
                elif stack == (len(self.topList) + 1) and direction != 'l':
                    raise Exception
                elif self.topList[stack] != '.' and direction == 'u':
                    raise Exception
                elif self.topList[stack] == '.' and direction == 'd':
                    raise Exception
                elif self.topList[stack] != '.' and direction == 'd' and self.stacks[stack - 1].isFull():
                    raise Exception
                elif direction == 'u' and self.stacks[stack - 1].isEmpty():
                    raise Exception
                elif direction in 'lr' and self.topList[stack] == '.':
                    raise Exception
                elif direction == 'l' and self.topList[stack - 1] != '.':
                    raise Exception
                elif direction == 'r' and self.topList[stack + 1] != '.':
                    raise Exception
                else:
                    return True
            except Exception:
                print("Error: Invalid move.")



    def isSolved(self, card):
        """
        This method checks the player's current board state against the configuration card by assembling the bounded
        stack elements into a string, and checking if it matches our configuration card string
        :param card: (str) - String representation of our configuration card
        :return: True if game board matches configuration card, else, returns False
        """

        card = card.replace('|', '')
        playerPuzzle = ''
        # This block loops through each stack and grabs copies of each bead in the stack in descending order
        for stack in self.stacks:
            for bead in range(self.depth - 1, -1, -1):
                playerPuzzle = playerPuzzle + stack.showBead(bead)
        if playerPuzzle == card:
            return True
        else:
            return False

    def show(self, card=None):
        """
        This method displays the current board state. If there is a card parameter passed in, it will also display the
        configuration card, as well as how many moves have been made
        :param card: (str) - This is the string representation of the configuration card
        :return: None
        """
        divider = "+" + "-"*(self.stackCount*2 + 1) + "+"
        for i in range(len(self.topList)):
            print(str(i) + ' ', end='')

        if card == None:

            top = ' '.join(self.topList)
            print()
            print(top)

            # For displaying the stacks, we loop through in descending order
            for bead in range(self.depth-1, -1, -1):
                line = ''
                for stack in self.stacks:
                    line = line + stack.showBead(bead)
                line = ' '.join(line)
                print('| ' + line + ' |')
            print(divider)
            print()

        else:
            card = card.replace('|','')
            card = list(card)
            top = ' '.join(self.topList)
            print()
            print("{0:17}{1}".format(top, 'card'))
            row = 0

            # For displaying the stacks, we loop through in descending order
            for bead in range(self.depth - 1, -1, -1):
                line = ''
                cardLine = ''
                target = row % self.stackCount
                row += 1

                for i in range(len(card)):
                    if i % self.depth == target:
                        cardLine = cardLine + card[i]
                for stack in self.stacks:
                    line = line + stack.showBead(bead)

                cardLine = ' '.join(cardLine)
                cardLine = '|' + cardLine + '|'
                line = ' '.join(line)
                line = '| ' + line + ' |'
                print("{0:15}{1}".format(line, cardLine))

            print("{0}{1:>24}".format(divider, str(self.moves) + ' moves'))
            print()



class BStack():
    """
    This is our Bounded Stack class. It has a capacity set by the user. The capacity is the depth of the stack,
    as determined by how many times a single color (letter) occurs.
    """

    def __init__(self, capacity):
        self.__capacity = capacity
        self.__items = []

    def push(self, item):
        """
        This method pushes a new item into our stack if our capacity is not reached
        :param item: (str) - The item to be pushed into our stack
        :return: None
        """
        if self.isFull():
            raise Exception('Stack is full.')
        self.__items.append(item)

    def pop(self):
        """
        This method pops an item out of our stack if there is an item to be removed.
        :return: Returns whatever element was ot the top of our stack, if any
        """
        if self.isEmpty():
            raise Exception('Stack is empty.')
        return self.__items.pop()

    def showBead(self, ind):
        """
        This method is used to display our board state by finding what is in the index (ind) of our stack
        :param ind: (int) - The index in which to return our stack element
        :return: Returns a copy of our stack element at the given index (ind), or '.' if no element present
        """
        empty = '.'
        if ind > len(self.__items)-1:
            return empty
        else:
            return self.__items[ind]

    def isEmpty(self):
        """
        This method checks to see if our stack is empy
        :return: Returns True if there no items in our stack, and False if there is at least one.
        """
        return len(self.__items) == 0

    def isFull(self):
        """
        Checks to see if our stack is full
        :return: True if our stack is at capacity, and False otherwise
        """
        return self.__capacity == len(self.__items)

class Card:
    """
    This class creates an interation of a Card for our game. It will fill with the given amount of 'Colors' as well as
    the provided depth for the stacks used in the game.
    """
    def __init__(self, depth, colors):
        """
        This function initialized our new instance of a Card class.
        :param self: card (Card): A card object
        :param depth: (int) - The depth of each stack for our game
        :param colors: (int) - The number of colors to be used for our card game
        :return: None
        """
        self.__beads = []
        self.depth = depth
        self.colorAmount = colors
       # self.size = self.depth*self.depth
        self.setColors()


    def setColors(self):
        """
        This function defines our 'colors' used for our card. Starting with 'A', our function gets a new letter for
        however many is specified by the user in the creation of the card. We then multiply the letter by the depth
        of the game as provided by the user and add all letters to our beads list.
        :return: None
        """
        alphabetList = list(string.ascii_uppercase)
        for i in range(self.colorAmount):
            self.__beads += alphabetList[i] * self.depth

    def getBeads(self):
        return self.__beads

    def getColors(self):
        return self.colorAmount

    def getDepth(self):
        return self.depth

    def reset(self):
        random.shuffle(self.__beads)

    def show(self):

        for color in range(self.colorAmount):
            line = ''
            target = color % self.colorAmount
            for i in range(len(self.__beads)):
                if i % self.colorAmount == target:
                    line = line + self.__beads[i]
            line = ' '.join(line)
            print("|" + line + "|")

    def stack(self, number):
        """
        This method creates our came stacks
        :param number: (int) - The number of bounded stacks to create
        :return: None
        """
        number = number - 1
        stack = [self.__beads[i] for i in range(len(self.__beads)) if i % self.colorAmount == number]


    def replace(self, filename, n):

        file = open(filename, 'r')
        lines = file.readlines()
        line = lines[n-1].strip()
        line = line.replace(' ', '')
        self.colorAmount = len(set(list(line)))
        self.depth = len(list(line))//self.colorAmount
       # self.size = len(list(line))
        self.__beads = []
        self.setColors()
        self.reset()


    def __str__(self):

        counter = 0
        cardString = "|"
        totalBeads = len(self.__beads)

        for i in range(totalBeads):
            cardString = cardString + self.__beads[i]
            counter += 1
            if counter % self.depth == 0 and counter < totalBeads:
                cardString = cardString + "||"
        cardString = cardString + "|"

        return cardString

def test():

    card = Card(3, 3)
    card.stack(1)
    card.stack(2)
    card.stack(3)
    print(card.__str__())
    card.replace("assignment3test.txt", 4)
    print(card.__str__())
    cardString = card.__str__()

    depth = card.getDepth()
    colors = card.getColors()
    beads = card.getBeads()
    abaco = AbacoStack(colors, depth, beads)
    abaco.moveBead('1u')
    abaco.show()
    abaco.moveBead('1l')
    abaco.show(cardString)
    abaco.reset()
    abaco.show()
    abaco.moveBead('3u')
    abaco.moveBead('3r')
    abaco.moveBead('3u')
    abaco.moveBead('3l')
    abaco.moveBead('2l')
    abaco.moveBead('2u')
    abaco.moveBead('2r')
    abaco.moveBead('3d')
   # abaco.moveBead('')
    print(abaco.stacks[2])
    abaco.show()

if __name__ == '__main__':
    test()

main()
