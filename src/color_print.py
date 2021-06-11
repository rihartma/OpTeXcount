class Printer:
    """
    Class for printing string with specific color
    Color list: blue, green, cyan, red, white
    """
    def __init__(self):
        self.__blue = '\033[1;34;48m'
        self.__green = '\033[1;32;48m'
        self.__cyan = '\033[1;36;48m'
        self.__red = '\033[1;31;48m'
        self.__terminate = '\033[1;37;0m'

    def print_c(self, text, color):
        print(color + text + self.__terminate, end='')

    def blue(self, text):
        self.print_c(text, self.__blue)

    def green(self, text):
        self.print_c(text, self.__green)

    def cyan(self, text):
        self.print_c(text, self.__cyan)

    def red(self, text):
        self.print_c(text, self.__red)

    def white(self, text):
        print(text, end='')
