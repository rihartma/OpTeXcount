import re
import tokens
import keywords


### TODO \par[some-tag] - resolve this situation


# ---------------------------------------------------------------------------------------------------------------------
class Result ():
    def __init__ (self):
        self.text_words = 0
        self.header_words = 0

    def increase (self, cathegory):
        if (cathegory.get_type () == 1):
            self.text_words += 1
        else:
            self.header_words += 1

    def __str__ (self):
        counts = "Words in text: " + str (self.text_words) + "\n"
        counts += "Words in headers: " + str (self.header_words) + "\n"
        return counts


class Cathegory ():
    def __init__ (self, t = 1):
        self.__type_id = t   # implicitely normal text
        # Hier can be added an extra class variables - utility extension where the programm counts and stores each subsections etc.

    def set_type (self, cathegory_id):
        self.__type_id = cathegory_id

    def get_type (self):
        return self.__type_id
# ---------------------------------------------------------------------------------------------------------------------

CURRENT_CATEGHORY = Cathegory ()
WORDS_COUNTS = Result ()

EOL = " EOL "


def is_keyword (word):
    if (word in keywords.key_words):
        return True
    return False


def process_word (word):
    if (word == EOL):
        CURRENT_CATEGHORY.set_type (1)

    elif (is_keyword (word)):
        cathegory = keywords.key_words [word]
        if (cathegory == 2):
            CURRENT_CATEGHORY.set_type (cathegory)
    
    else:
        print (word)
        WORDS_COUNTS.increase (CURRENT_CATEGHORY)


def read_words (line):
    '''
    Parses a line of a source code passed by argument using regular expressions.
    It seperates each word on the line and stores it in the list.
    All non escape occurances of charackters {}[] are seperated to be a single "words"
    All escape alphabetic characters are separated from the previous word
    At the end of each line it genererates end of line signalization - EOL
    '''

    line = re.sub (r'(?<!\\)(?:\\\\)*([{}\[\]])', r' \1 ', line)
    line = re.sub (r'(?<!\\)(\\\\)*(\\)([A-Za-z])', r'\1 \2\3', line)
    words_on_line = re.split ("\s+", line)
    words_on_line.append (EOL)
    return words_on_line


"""
Reads a file with filename passed by parameter.
It reads the file word by word and processes the loaded word
"""
def analyze_file (filename):
    with open (filename, 'r') as file:
        for line in file:
            for word in read_words (line):
                process_word (word)



keywords.initialize ()

def main():
    print (read_words ("It's only somé ddd\\\\try and, {another tr}y. What if \\\\\\key\\key"))
    # analyze_file ("../examples/header_sections.tex")
    # print (WORDS_COUNTS)


if __name__ == "__main__":
    main()

