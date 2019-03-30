import AIEntity
import numpy as np
import argparse
import copy
import random


# Prepares parser for initial options (for testing stuff)
def prep_parser():
    parser = argparse.ArgumentParser(description="Master Mind Game with AI I guess")

    parser.add_argument("-c", "--code", dest="code_gen",
                        help="The way the goal code is generated (random or manual), default = random",
                        default="random")

    parser.add_argument("-n", "--ncolors", dest="all_colors",
                        help="Number of total available colors", default="5")

    parser.add_argument("-p", "--nPegs", dest="nPegs",
                        help="Number of pegs (holes)", default="4")

    options = parser.parse_args()

    return options


# Makes the human choose a color
def human_choose_color(total_colors, n_pegs):
    goal_code = np.zeros((n_pegs,), dtype=int)

    print("Available colors: " + str(total_colors))
    print("Choose goal color code: ")

    inserted = 0
    while inserted < n_pegs:
        color = int(input("Color " + str(inserted + 1) + ": "))
        if 0 < color <= total_colors:
            goal_code[inserted] = color
            inserted = inserted + 1
        else:
            print("Enter a valid color, available colors: " + str(total_colors))
    print(goal_code)
    return goal_code


###         functions of the board      ###

# Just creates the [Black, Black, Black, Black] info
def generate_goal_info(n_pegs):
    goal = []
    for peg in range(n_pegs):
        goal.append(1)

    return goal


# Returns the "black and white" info by comparing guess and code_comp params
def gen_info(new_guess, code_comp):
    info = []
    black = 0
    white = 0
    peg_number = len(new_guess)

    # Converting guess and code to arrays to operate with them
    new_guess = np.array(new_guess)
    code_comp = np.array(code_comp)

    # Creating empty info
    for peg in range(peg_number):
        info.append(None)

    # info = np.array(info)

    peg_compare = copy.deepcopy(new_guess)
    code_compare = copy.deepcopy(code_comp)

    for peg in range(peg_number):
        if peg_compare[peg] == code_compare[peg]:
            black += 1
            peg_compare[peg] = 0
            code_compare[peg] = -1

    for peg in range(peg_number):
        for j in range(peg_number):
            if (code_compare[peg] == peg_compare[j]) and (peg != j):
                white += 1
                peg_compare[j] = 0
                code_compare[peg] = -1
                break

    for peg in range(black):
        info[peg] = 1

    for peg in range(black, black + white):
        info[peg] = 0

    return info


# Generates goal code randomly
def generate_code(total_colors, peg_number):
    goal_code = []
    colors = []

    for i in range(1, total_colors + 1):
        colors.append(i)

    for p in range(peg_number):
        goal_code.append(random.choice(colors))

    # code = np.random.randint(1,high=allColors + 1, size=nPegs)
    return goal_code


##      main program    ##
if __name__ == "__main__":

    options = prep_parser()
    nPegs = int(options.nPegs)
    goal_info = generate_goal_info(nPegs)
    all_colors = int(options.all_colors)

    if options.code_gen == "random":
        code = generate_code(all_colors, nPegs)  # code will be generate randomly
    else:
        code = human_choose_color(all_colors, nPegs)  # code will be selected by human

    print(goal_info)

    # Creating AI entity
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
