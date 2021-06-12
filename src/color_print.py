class Printer:
    """
    Class for printing string with specific color
    Color list: blue, green, cyan, red, white
    """
    def __init__(self):
        self.__BLUE = '\033[1;34;48m'
        self.__GREEN = '\033[1;32;48m'
        self.__CYAN = '\033[1;36;48m'
        self.__RED = '\033[1;31;48m'
        self.__TERM = '\033[1;37;0m'

    def print_c(self, text, color):
        print(color + text + self.__TERM, end='')

    def blue(self, text):
        self.print_c(text, self.__BLUE)

    def green(self, text):
        self.print_c(text, self.__GREEN)

    def cyan(self, text):
        self.print_c(text, self.__CYAN)

    def red(self, text):
        self.print_c(text, self.__RED)

    def white(self, text):
        print(text, end='')
