class bcolors:
    def __init__(self):
        self.RED = '\033[41m'
        self.BLUE = '\033[44m'
        self.GREEN = '\033[42m'
        self.YELLOW = '\033[43m'
        self.WHITE = '\033[47m'
        self.ENDC = '\033[0m'

    #returns ansi color depending on the input
    def ret_ansi(self, color):
        if color == "red":
            return self.RED
        elif color == "blue":
            return self.BLUE
        elif color == "green":
            return self.GREEN
        elif color == "yellow":
            return self.YELLOW
        elif color == "white":
            return self.WHITE
        return self.ENDC
