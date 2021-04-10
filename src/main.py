import re
import keywords as kw


kw.initialize ()


example_file = open ("../examples/example1.tex", "r")


allwords = []

def parse (line):

    word_seps = " \t{}();:?!\n"
    begin = end = 0

    while (begin < len (line)):
        if (line[begin] in word_seps):
            begin += 1
            continue

        end = begin + 1

        while (end < len (line)):
            if (line [end] in word_seps):
                break;
            end += 1

        allwords.append (line[begin:end])
        begin = end

    print ("Line parsed: ")
    print (allwords)


while (True):
    line = example_file.readline()
    if (line == ""):
        break
    parse (example_file.readline())

