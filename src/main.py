import re
import keywords


keywords.initialize ()


def is_keyword (word):
    if (word in keywords.key_words):
        return True
    return False


def process_word (word):
    if (is_keyword (word)):
        print (word + " KEYWORD!")
    else:
        print (word + " normal text word")

def read_words (line):

    words_on_line = []

    word_seps = " ();:?!\n"
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

        words_on_line.append (line[begin:end])
        begin = end

    return words_on_line


def run (filename):
    
    with open (filename, 'r') as file:
        for line in file:
            for word in read_words (line):
                process_word (word)

run ("../examples/header_sections.tex")
