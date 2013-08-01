from __future__ import division, print_function
from Game import Game
from bots import *
from Player import Player
from titForTat import TitForTatter
import sys, termios, tty

# store stdin's file descriptor
stdinFileDesc = sys.stdin.fileno()
# save stdin's tty attributes so I can reset it later
oldStdinTtyAttr = termios.tcgetattr(stdinFileDesc)

if __name__ == '__main__':
    # introduce some players in the game
    players = [Player(), Pushover(), Freeloader(), Alternator(), MaxRepHunter(), Random(.2),
            Random(.8), TitForTatter()]
    game = Game(players)

    print('==== Round-stepped game, press q to quit and any other key to continue ====\n')
    try:
        print('Press any key to exit...')
        while True:
            try:
                game.play_round()
            except StopIteration:
                break

            # set the input mode of stdin so that it gets added to char by char rather than line by line
            tty.setraw(stdinFileDesc)
            # read 1 byte from stdin (indicating that a key has been pressed)
            c = sys.stdin.read(1)
            # reset stdin to its normal behavior
            termios.tcsetattr(stdinFileDesc, termios.TCSADRAIN, oldStdinTtyAttr)
            if c == 'q':
                print('\n==== Game finished by the user, goodbye! ====')
                break
    finally:
        # reset stdin to its normal behavior
        termios.tcsetattr(stdinFileDesc, termios.TCSADRAIN, oldStdinTtyAttr)

