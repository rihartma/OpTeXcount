import re
import keywords as kw


kw.initialize ()


example_file = open ("../examples/priklad-optex.tex", "r")


def parse (line):
    print (line, end="")


while (True):
    line = example_file.readline()
    if (line == ""):
        break
    parse (example_file.readline())

