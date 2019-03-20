from AIEntity import AIEntity
import numpy as np
import argparse
import copy

#prepare parser for initial options (for testing stuff)
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game with AI I guess")

    parser.add_argument("-c","--code",dest="code_gen",
        help="The way the goal code is generated (random or manual), default = random",default="random")

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

#Just creates the [Black, Black, Black, Black] info
def generate_goal_info(nPegs):
    goal_info = []
    for i in range(nPegs):
        goal_info.append(1);

    return goal_info

#Generates goal code randomly
def generate_code(allColors,nPegs):

    code = np.random.randint(1,high=len(allColors) + 1, size=nPegs)
    return code

##      main program    ##
if __name__== "__main__":

    allColors = ["red", "yellow", "blue", "green", "white"] #available colors
    nPegs = 4   #number of holes
    options = prep_parser()
    goal_info = generate_goal_info(nPegs)
    if options.code_gen == "random":
        code = generate_code(allColors, nPegs) #code will be generate randomly
    else:
        code = human_choose_color(allColors, nPegs) #code will be selected by human

    #Creating AI entity
    AI = AIEntity(len(allColors), nPegs)

    print(str(code) + "<---Code")
    print("-------------Guesses-------------")

    for i in range(10):
        guess = AI.guess()
        AI.info = AI.gen_info(code, guess)
        print(guess, AI.info)
        AI.reduce_pool()
        if AI.info == goal_info:#np.array_equal(np.array(goal_info),AI.info):
            print("AI wins the game")
            break
