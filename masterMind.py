#!/usr/bin/env python3

import argparse
import sys
import ANSIColors as AC

#prepare parser for initial options
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game")

    parser.add_argument("-p1","--player1",dest="player1",
        help="Player 1 who CHOOSSES goal colors (me or ai)",default="me")

    parser.add_argument("-p2","--player2",dest="player2",
        help="Player 2 who GUESSES goal colors (me or ai)",default="me")
    return parser


def human_choose_color(allColors,nPegs):
    code = []
    print("Available colors: " + str(allColors))
    print("Choose goal color code: ")

    i = 0
    while i < nPegs:
        color = input("Color " + str(i+1) + ": ")
        if color in allColors:
            code.append(color)
            i = i + 1
        else:
            print("Enter a valid color, available colors: " + str(allColors))

    return code

#print any code given with colors!
def print_code(code, ansiColors):
    for color in code:
        ansi = ansiColors.ret_ansi(color)
        print( ansi + "o" + ansiColors.ret_ansi("ENDC") + " ", end="")
    print("")


##      main program    ##
if __name__== "__main__":
    ansiColors = AC.bcolors()
    colors  = ["red","yellow","blue","green","white"]
    nPegs   = 4 #number of positions
    parser  = prep_parser()
    options = parser.parse_args()

    if options.player1 == "me":
        code = human_choose_color(colors,nPegs)

    print("\nCode: " + str(code))

    print ("Selected code: ")

    print_code(code,ansiColors)
