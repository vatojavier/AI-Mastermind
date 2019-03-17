import AIEntity
import numpy as np
import argparse
import copy

#prepare parser for initial options (for testing stuff)
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game with AI I guess")

    parser.add_argument("-c","--code",dest="code_gen",
        help="The way the goal code is generated (random or me), default = random",default="random")

    options = parser.parse_args()

    return options

#makes the human choose a color
def human_choose_color(allColors,nPegs):

    code = np.zeros((nPegs,), dtype=int)

    print("Available colors: " + str(len(allColors)))
    print("Choose goal color code: ")

    i = 0
    while i < nPegs:
        color = int(input("Color " + str(i+1) + ": "))
        if (color > 0 and color <= len(allColors)):
            code[i] = color
            i = i + 1
        else:
            print("Enter a valid color, available colors: " + str(len(allColors)))
    print(code)
    return code

###         functions of the board      ###

#generate goal code randomly
def generate_code(allColors,nPegs):

    code = np.random.randint(1,high=len(allColors) + 1, size=nPegs)
    return code

#compares code and guess and returns black and whites stuff
def gen_info(guess,code):
    info = [None,None,None,None]
    black = 0
    white = 0
    peg_compare = copy.deepcopy(guess)
    code_compare = copy.deepcopy(code)

    for i in range(4):
        if peg_compare[i] == code_compare[i]:
            black += 1
            peg_compare[i] = 0
            code_compare[i] = -1

    for i in range(4):
        for j in range(4):
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


##      main program    ##
if __name__== "__main__":

    allColors = ["red","yellow","blue","green","white"] #available colors
    nPegs = 4   #number of holes
    options = prep_parser()

    if options.code_gen == "random":
        code = generate_code(allColors,nPegs) #code will generate randomly
    else:
        code = human_choose_color(allColors,nPegs) #code selected by human

    AI = AIEntity.AIEntity(len(allColors),nPegs) #Creating AI entity
    print(str(code) + "<---Code")

    for i in range(10):
        guess = AI.guess()
        AI.info = gen_info(code,guess)
        print(guess , AI.info)
