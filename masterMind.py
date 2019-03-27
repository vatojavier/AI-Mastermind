import AIEntity
import numpy as np
import argparse
import copy
import random

#Prepares parser for initial options (for testing stuff)
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game with AI I guess")

    parser.add_argument("-c","--code",dest="code_gen",
        help="The way the goal code is generated (random or manual), default = random",default="random")

    parser.add_argument("-n","--ncolors",dest="all_colors",
        help="Number of total available colors",default="5")

    parser.add_argument("-p","--nPegs",dest="nPegs",
        help="Number of pegs (holes)",default="4")

    options = parser.parse_args()

    return options

#Makes the human choose a color
def human_choose_color(all_colors,nPegs):

    code = np.zeros((nPegs,), dtype=int)

    print("Available colors: " + str(all_colors))
    print("Choose goal color code: ")

    i = 0
    while i < nPegs:
        color = int(input("Color " + str(i+1) + ": "))
        if (color > 0 and color <= all_colors):
            code[i] = color
            i = i + 1
        else:
            print("Enter a valid color, available colors: " + str(all_colors))
    print(code)
    return code


###         functions of the board      ###

#Just creates the [Black, Black, Black, Black] info
def generate_goal_info(nPegs):
    goal_info = []
    for i in range(nPegs):
        goal_info.append(1);

    return goal_info

#Returns the "black and white" info by comparing guess and code params
def gen_info(guess, code):
    info = []
    black = 0
    white = 0
    nPegs = len(guess)

    #Converting guess and code to arrays to operate with them
    guess = np.array(guess)
    code = np.array(code)

    #Creating empy info     REMOVES HARDCODE BUT SLOW, MAYBE ENTER PARMETER AS ARRAY INSTEAD
    for i in range(nPegs):
        info.append(None)

    #info = np.array(info)

    peg_compare = copy.deepcopy(guess)
    code_compare = copy.deepcopy(code)

    for i in range(nPegs):
        if peg_compare[i] == code_compare[i]:
            black += 1
            peg_compare[i] = 0
            code_compare[i] = -1

    for i in range(nPegs):
        for j in range(nPegs):
            if (code_compare[i] == peg_compare[j]) and (i != j):
                white += 1
                peg_compare[j] = 0
                code_compare[i] = -1
                break

    for i in range(black):
        info[i] = 1

    for i in range(black, black + white):
        info[i] = 0

    return info

#Generates goal code randomly
def generate_code(allColors,nPegs):
    code = []
    colors = []

    for i in range (1,allColors + 1):
        colors.append(i)

    for p in range(nPegs):
        code.append(random.choice(colors))

    #code = np.random.randint(1,high=allColors + 1, size=nPegs)
    return code

##      main program    ##
if __name__== "__main__":

    options = prep_parser()
    nPegs = int(options.nPegs)
    goal_info = generate_goal_info(nPegs)
    all_colors = int(options.all_colors)


    if options.code_gen == "random":
        code = generate_code(all_colors, nPegs) #code will be generate randomly
    else:
        code = human_choose_color(all_colors, nPegs) #code will be selected by human


    print(goal_info)


    #Creating AI entity
    AI = AIEntity.AIEntity(all_colors, nPegs)

    print(str(code) + "<---Code")
    print("-------------Guesses-------------")
    for i in range(10):
        guess = AI.smart_guess()
        AI.info = gen_info(code, guess)
        print(guess, AI.info)
        AI.reduce_pool()

        if AI.info == goal_info:
            print("AI wins the game")
            break
