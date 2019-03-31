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

    parser_options = parser.parse_args()

    return parser_options


# Makes the human choose a color
def human_choose_color(total_colors, peg_number):
    new_code = np.zeros((peg_number,), dtype=int)

    print("Available colors: " + str(total_colors))
    print("Choose goal color code: ")

    inserted = 0
    while inserted < peg_number:
        color = int(input("Color " + str(inserted + 1) + ": "))
        if 0 < color <= total_colors:
            new_code[inserted] = color
            inserted = inserted + 1
        else:
            print("Enter a valid color, available colors: " + str(total_colors))
    print(new_code)
    return new_code


#        functions of the board      #

# Just creates the [Black, Black, Black, Black] info
def generate_goal_info(n_pegs):
    goal = []
    for peg in range(n_pegs):
        goal.append(1)

    return goal


# Returns the "black and white" info by comparing guess and code params
def gen_info(guess, code_comp):
    info = []
    black = 0
    white = 0
    peg_number = len(guess)

    # Converting guess and code to arrays to operate with them
    guess = np.array(guess)
    code_comp = np.array(code_comp)

    # Creating empty info
    for peg in range(peg_number):
        info.append(None)

    # info = np.array(info)

    peg_compare = copy.deepcopy(guess)
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

    for new_color in range(1, total_colors + 1):
        colors.append(new_color)

    for p in range(peg_number):
        goal_code.append(random.choice(colors))

    # code = np.random.randint(1,high=allColors + 1, size=nPegs)
    return goal_code


#      main program    #
if __name__ == "__main__":

    options = prep_parser()
    nPegs = int(options.nPegs)
    goal_info = generate_goal_info(nPegs)
    all_colors = int(options.all_colors)

    if options.code_gen == "random":
        code = generate_code(all_colors, nPegs)  # code will be generate randomly
    else:
        code = human_choose_color(all_colors, nPegs)  # code will be selected by human

    AI = AIEntity.AIEntity(all_colors, nPegs)
    original_pool = AI.pool

    guess_array = []
    for code in original_pool:
        AI.pool = original_pool
        AI.step = 0
        guess = 0
        print(str(code) + "<---Code")
        print("-------------Guesses-------------")
        for i in range(10):

            best_guess = AI.random_guess()
            guess += 1
            AI.info = gen_info(code, best_guess)  # Actual guess played
            print(AI.new_guess, AI.info)
            AI.reduce_pool()
            if AI.info == goal_info:
                print("AI wins the game")
                guess_array.append(guess)
                break

    average = sum(guess_array) / len(original_pool)
    worst_case = max(guess_array)
    print("Average guess for naive AI: " + str(average) + " worst case: " + str(worst_case))
