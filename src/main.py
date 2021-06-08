import re
import keywords as kw

### -----------------------------------------------------------------------------------------------
class WordIterator:
    '''
    A basic wrapper for sequentional reading of words from file
    '''

    def __init__(self, filename):
        self.filename = filename
        self.word_queue = []
        self.line_payload = 50  # how many lines will be loaded into the queue at one time
        self.__load_line = 1    # which line haven't been already loaded into the queue


    def read(self):
        '''
        Returns word first word that wasn't already read by this particular object
        '''
        if (len(self.word_queue) == 0):
            self.__load_payload()
        if (len(self.word_queue) == 0):
            return None
        else:
            return self.word_queue.pop(0)


    def push_back(self, word):
        '''
        Pushes word from argument into the first position of the queue
        In case we already read a word but we want to re-read it again
        '''
        self.word_queue = [word] + self.word_queue


    def __load_payload(self):
        '''
        Loads words from input file into the queue
        '''
        index = 0
        with open (self.filename, 'r') as file:
            for line in file:
                index += 1
                if (index < self.__load_line):
                    continue
                elif (index < self.__load_line + self.line_payload):
                    self.word_queue += self.__parse_words(line)
                else:
                    break
        self.__load_line = index + 1

    def __parse_words (self, line):
        '''
        Parses a line passed by argument using regular expressions.
        It seperates each word on the line and stores it into list.
        All non escape occurances of charackters {}[] are seperated to be a single 'word'
        All escaped alphabetic characters are separated from the previous word
        At the end of every nonempty line newline character is placed
        TODO separate commentary - %
        '''
        if (line == "\n" or line == "\r\n" ):
            return []
        line = re.sub (r'(?<!\\)(?:\\\\)*([{}\[\]])', r' \1 ', line)
        line = re.sub (r'(?<!\\)(\\\\)*(\\)([A-Za-z])', r'\1 \2\3', line)
        words_on_line = re.split ("\s+", line)
        words_on_line.append ("\n")
        return list(filter(lambda it: it != '', words_on_line))

### -----------------------------------------------------------------------------------------------

class Header:
    def __init__(self, header_type):
        self.type = header_type # title, chapter, section, subsection
        self.words = []
        self.header_count = 0
        self.text_count = 0

    def add_header_word(self, word):
        self.words.append(word)
        self.header_count += 1

    def add_text_word(self, word):
        self.text_count += 1

    def __str__(self):
        result = self.type + " ("
        result += str(self.header_count) + " + " + str(self.text_count) + ")"
        for word in self.words:
            result += " " + word
        return result

### -----------------------------------------------------------------------------------------------

class Counter:
    '''
    Class that analyzes a source code and counts word counts
    '''

    def __init__ (self, filename):
        self.word_iter = WordIterator(filename) # source of words that will be analyzed
        self.regular_words_count = 0
        self.header_words_count = 0
        self.all_headers = []
        self.__context = "regular-text"


    def run (self):
        '''
        Main method of the class
        Loads all words and initializes the analysis
        '''
        word = self.word_iter.read()
        while (word != "\\bye" and word != None):
            self.__process_word(word)
            word = self.word_iter.read()
        #return [self.regular_words_count, self.header_words_count]

    def print_result (self):
        '''
        Generates formated output of the counter
        '''
        print ("Text words summary: " + str(self.regular_words_count))
        print ("Header words summary: " + str(self.header_words_count))
        print ("Subcounts: (header-words-count + text-words-count)")
        for header in self.all_headers:
            print (header)


    def __process_word(self, word):
        '''
        Decides how to treat with word from argument
        '''
        if (word == "%"):
            self.__skip_commentary()
        elif (word == "\n"):
            return
        elif (word == "{"):
            self.__load_curly_brackets()
        elif (self.__is_keyword(word)):
            self.__process_keyword(word)
        else:
            self.__process_text_word(word)


    def __process_keyword(self, word):
        if (word == '\\tit'):
            self.all_headers.append(Header("title"))
            self.__load_header()
        elif (word == '\\chap'):
            self.all_headers.append(Header("chapter"))
            self.__skip_square_brackets()
            self.__load_header()
        elif (word == '\\sec'):
            self.all_headers.append(Header("section"))
            self.__skip_square_brackets()
            self.__load_header()
        elif (word == '\\secc'):
            self.all_headers.append(Header("subsection"))
            self.__skip_square_brackets()
            self.__load_header()
        elif (word == '\\begitems'):
            self.__load_list()
        elif (word in kw.keywords_list):
            self.__read_arguments(word)
        else:
            pass
            # skip unkwown keywords



    def __process_text_word(self, word):
        if (self.__context == "regular-text"):
            self.regular_words_count += 1
            if (len(self.all_headers)):
                self.all_headers[-1].add_text_word(word)
        elif (self.__context == "header"):
            self.header_words_count += 1
            self.all_headers[-1].add_header_word(word)


    def __is_keyword(self, word):
        if (len(word) >= 3):
            if (word[0] == '\\' and word[1].isalpha() and word[2].isalpha()):
                return True
        return False


    # def __known_keyword(self, word):
    #     if (word in kw.keywords_list):
    #         return True
    #     return False


    def __load_header(self):
        orig_context = self.__context
        self.__context = 'header'
        word = self.word_iter.read()
        skip_new_line = False
        while (word != None and word != "\\bye"):
            if (word == "\n"):
                if (not skip_new_line):
                    self.__context = orig_context
                    return
            elif (word == "^^J"):
                skip_new_line = True
            else:
                self.__process_word(word)
                skip_new_line = False
            word = self.word_iter.read()
        self.__context = orig_context

    def __load_list(self):
        word = self.word_iter.read()
        while (word != "\\enditems"):
            if (word == None):
                raise Exception("No list ending found - \\enditems")
            if (word != "*"):
                self.__process_word(word)
            word = self.word_iter.read()


    def __read_arguments(self, word):
        params = kw.keywords_list[word]
        for p in params:
            if (p == "O"):
                pass
            elif (p == "W"):
                self.__obligatory_argument()
            elif (p == "S"):
                self.__optional_argument()
                # is it voluntary or not ??? !!! IMPORTANT
            elif (p == "P"):
                pass
            elif (p == "C"):
                # skip brackets or load them??? TODO
                self.__skip_curly_brackets()
            else: # unknown specifier - no argument expected
                pass


    def __obligatory_argument(self):
        word = self.word_iter.read()
        if (word == None or word == "\\bye"):
            raise Exception("No obligatory argument found")
        return word


    def __optional_argument(self):
        word = self.word_iter.read()
        if (word != "["):
            self.word_iter.push_back(word)
            return None
        else:
            self.__skip_square_brackets()


    def __load_curly_brackets(self):
        word = self.word_iter.read()
        while (word != "}"):
            if (word == None):
                raise Exception("No closing bracket ('}') found.")
            self.__process_word(word)
            word = self.word_iter.read()


    def __skip_curly_brackets(self):
        word = self.word_iter.read()
        while (word != "}"):
            if (word == None):
                raise Exception("No closing bracket ('}') found.")
            word = self.word_iter.read()


    def __skip_square_brackets(self):
        word = self.word_iter.read()
        while (word != "]"):
            if (word == None):
                raise Exception("No closing bracket (']') found.")
            word = self.word_iter.read()


    def __skip_commentary(self):
        word = self.word_iter.read()
        while (word != None and word != "\n"):
            word = self.word_iter.read()



def main():
    counter = Counter("../tests/test-04.tex")
    counter.run()
    counter.print_result()

if __name__ == "__main__":
    main()

