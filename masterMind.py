from AIEntity import AIEntity
import numpy as np
import argparse
import copy

#Prepares parser for initial options (for testing stuff)
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game with AI I guess")

    parser.add_argument("-c","--code",dest="code_gen",
        help="The way the goal code is generated (random or manual), default = random",default="random")

    parser.add_argument("-n","--ncolors",dest="all_colors",
        help="Number of total available colors",default="5")

    parser.add_argument("-p","--pegs",dest="nPegs",
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
    for i in range(nPegs + 1):
        goal_info.append(1);

    return goal_info

#Generates goal code randomly
def generate_code(allColors,nPegs):

    code = np.random.randint(1,high=allColors + 1, size=nPegs)
    return code

##      main program    ##
if __name__== "__main__":

    nPegs = 4   #number of holes
    options = prep_parser()
    goal_info = generate_goal_info(nPegs)
    print(goal_info)
    all_colors = int(options.all_colors)
    nPegs = int(options.nPegs)

    if options.code_gen == "random":
        code = generate_code(all_colors, nPegs) #code will be generate randomly
    else:
        code = human_choose_color(all_colors, nPegs) #code will be selected by human

    #Creating AI entity
    AI = AIEntity(all_colors, nPegs)

    print(str(code) + "<---Code")
    print("-------------Guesses-------------")

    for i in range(10):
        guess = AI.guess()
        AI.info = AI.gen_info(code, guess)
        print(guess, AI.info)
        AI.reduce_pool()
        if AI.info == goal_info:
            print("AI wins the game")
            break
