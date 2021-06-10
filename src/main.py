import re
import keywords as kw

# TODO margin count thinks that shouldnt be counted
# TODO count verbatim words as text, not keywords

class WordIterator:
    """
    A basic wrapper for sequential reading of words from file
    """

    def __init__(self, filename):
        self.filename = filename
        self.word_queue = []
        self.line_payload = 50  # how many lines will be loaded into the queue at one time
        self.__load_line = 1  # index of first line which haven't been already loaded into the queue

    def read(self):
        """
        Returns first word from file that wasn't already read by this particular object
        """
        if len(self.word_queue) == 0:
            self.__load_payload()
        if len(self.word_queue) == 0:
            return None
        else:
            return self.word_queue.pop(0)

    def push_back(self, word):
        """
        Pushes word from argument into the first position of the queue
        In case we already read a word but we want to re-read it again
        """
        self.word_queue = [word] + self.word_queue

    def __load_payload(self):
        """
        Loads words from input file into the queue
        """
        index = 0
        with open(self.filename, 'r') as file:
            for line in file:
                index += 1
                if index < self.__load_line:
                    continue
                elif index < self.__load_line + self.line_payload:
                    self.word_queue += self.__parse_words(line)
                else:
                    break
        self.__load_line = index + 1

    @staticmethod
    def __parse_words(line):
        """
        Parses a line passed by argument using regular expressions.
        It separates each word on the line and stores it into list.
        """

        if line == "\n" or line == "\r\n":
            return []
        # All non escape occurrences of some characters are seperated to be a single 'word'
        line = re.sub(r'(?<!\\)(?:\\\\)*([{}\[\]()%])', r' \1 ', line)
        # $$ and $ are separated from the text to be a single 'word'
        line = re.sub(r'(?<!\\)(?:\\\\)*((\$\$)|(\$))', r' \1 ', line)
        # All escaped alphabetic characters are separated from the previous word
        line = re.sub(r'(?<!\\)(\\\\)*(\\)([A-Za-z])', r'\1 \2\3', line)
        words_on_line = re.split("\s+", line)
        # At the end of every nonempty line newline character is placed
        words_on_line.append("\n")
        return list(filter(lambda it: it != '', words_on_line))


class Header:
    def __init__(self, header_type):
        self.type = header_type  # title, chapter, section, subsection
        self.words = []
        self.header_count = 0
        self.text_count = 0
        self.caption_count = 0

    def add_header_word(self, word):
        self.words.append(word)
        self.header_count += 1

    def add_text_word(self, word):
        self.text_count += 1

    def add_caption_word(self, word):
        self.caption_count += 1

    def __str__(self):
        result = "  " + self.type + " ("
        result += str(self.header_count) + " + " + str(self.text_count) + " + " + str(self.caption_count) + ")"
        for word in self.words:
            result += " " + word
        return result


class Counter:
    """
    Class that analyzes a source code and counts word counts
    """

    def __init__(self, filename):
        self.word_iter = WordIterator(filename)  # source of words that will be analyzed
        self.regular_words_count = 0
        self.header_words_count = 0
        self.caption_words_count = 0
        self.figure_float_count = 0
        self.math_inline_count = 0
        self.math_count = 0
        self.all_headers = []
        self.__context = "regular-text"

    def run(self):
        """
        Main method of the class
        Loads all words and initializes the analysis
        """
        word = self.word_iter.read()
        while word != "\\bye" and word is not None:
            self.__process_word(word)
            word = self.word_iter.read()

    def print_result(self):
        """
        Generates formatted output of the counter
        """
        print("Text words summary: " + str(self.regular_words_count))
        print("Header words summary: " + str(self.header_words_count))
        print("Caption and notes words summary: " + str(self.caption_words_count))
        print("Headers summary: " + str(len(self.all_headers)))
        print("Figure/float count: " + str(self.figure_float_count))
        print("Inline math formulae count: " + str(self.math_inline_count))
        print("Math formulae count: " + str(self.math_count))
        print("Subcounts: (header-words-count + text-words-count + caption-words-count)")
        for header in self.all_headers:
            print(header)

    def __process_word(self, word):
        """
        Decides how to treat with word from argument
        """
        if word == "%":
            self.__skip_commentary()
        elif word == "\n":
            return
        elif word == "{":
            self.__load_curly_brackets()
        elif word == "$":
            self.__load_inline_formulae()
        elif word == "$$":
            self.__load_formulae()
        elif self.__is_keyword(word):
            self.__process_keyword(word)
        else:
            self.__process_text_word(word)

    def __process_keyword(self, word):
        word, arg = self.__split_keyword(word)
        if word == '\\tit':
            self.all_headers.append(Header("title"))
            self.__load_header()
        elif word == '\\chap':
            self.all_headers.append(Header("chapter"))
            self.__skip_brackets("[", "]")
            self.__load_header()
        elif word == '\\sec':
            self.all_headers.append(Header("section"))
            self.__skip_brackets("[", "]")
            self.__load_header()
        elif word == '\\secc':
            self.all_headers.append(Header("subsection"))
            self.__skip_brackets("[", "]")
            self.__load_header()
        elif word == '\\begitems':
            self.__load_list()
        elif word == '\\caption':
            self.__skip_brackets("[", "]")
            self.__load_caption()
        elif word == '\\fnote' or word == '\\fnotetext' or word == '\\mnote':
            self.__load_footnote()
        elif word in kw.keywords_list:
            if word in ["\\table", "\\inspic"]:  # TODO this should be in keywords file
                self.figure_float_count += 1
            self.__read_arguments(word)
        else:
            pass
            # skip unknown keywords

    def __process_text_word(self, word):
        if len(word) == 1 and not word.isalnum():
            return
        if self.__context == "regular-text":
            self.regular_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_text_word(word)
        elif self.__context == "header":
            self.header_words_count += 1
            self.all_headers[-1].add_header_word(word)
        elif self.__context == "caption":
            self.caption_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_caption_word(word)

    @staticmethod
    def __is_keyword(word):
        if len(word) >= 3:
            if word[0] == '\\' and word[1].isalpha() and word[2].isalpha():
                return True
        return False

    @staticmethod
    def __split_keyword(word):
        for i in range(1, len(word)):
            if not word[i].isalpha():
                return word[:i], word[i:]
        return word, ""

    def __load_header(self):
        orig_context = self.__context
        self.__context = 'header'
        word = self.word_iter.read()
        skip_new_line = False
        while word is not None and word != "\\bye":
            if word == "\n":
                if not skip_new_line:
                    self.__context = orig_context
                    return
            elif word == "^^J":
                skip_new_line = True
            else:
                self.__process_word(word)
                skip_new_line = False
            word = self.word_iter.read()
        self.__context = orig_context

    def __load_list(self):
        word = self.word_iter.read()
        while word != "\\enditems":
            if word is None:
                raise Exception("No list ending found - \\enditems")
            if word != "*":
                self.__process_word(word)
            word = self.word_iter.read()

    def __load_caption(self):
        orig_context = self.__context
        self.__context = 'caption'
        word = self.word_iter.read()
        while word is not None and word != "\\bye":
            if word == "\n":
                self.__context = orig_context
                return
            else:
                self.__process_word(word)
            word = self.word_iter.read()
        self.__context = orig_context

    def __load_footnote(self):
        orig_context = self.__context
        self.__context = 'caption'
        if self.word_iter.read() != "{":
            return
        self.__load_curly_brackets()
        self.__context = orig_context

    def __load_formulae(self):
        word = self.word_iter.read()
        while word != "$$":
            if word is None:
                raise Exception("No end of math formulae found!")
            word = self.word_iter.read()
        self.math_count += 1

    def __load_inline_formulae(self):
        word = self.word_iter.read()
        while word != "$":
            if word is None:
                raise Exception("No end of inline math formulae found!")
            word = self.word_iter.read()
        self.math_inline_count += 1

    def __read_arguments(self, word):
        params = kw.keywords_list[word]
        for p in params:
            if p == "O":
                pass  # this case is managed by '__process_keyword' method
            elif p == "W":
                self.__obligatory_argument()
            elif p == "S":
                self.__skip_brackets("[", "]")
            elif p == "P":
                self.__skip_brackets("(", ")")
            elif p == "C":
                self.__skip_brackets("{", "}")
            else:  # unknown specifier - no argument expected
                pass

    def __obligatory_argument(self):
        word = self.word_iter.read()
        if word is None or word == "\\bye":
            raise Exception("No obligatory argument found")
        return word

    # def __optional_argument(self):
    #     word = self.word_iter.read()
    #     if word != "[":
    #         self.word_iter.push_back(word)
    #         return None
    #     else:
    #         self.__skip_brackets("[","]")

    def __load_curly_brackets(self):
        word = self.word_iter.read()
        while word != "}":
            if word is None:
                raise Exception("No closing bracket ('}') found.")
            self.__process_word(word)
            word = self.word_iter.read()

    def __skip_brackets(self, opening, closing):
        word = self.word_iter.read()
        bracket_count = 0
        while True:
            if word is None:
                raise Exception("No closing bracket ('" + closing + "') found.")
            elif word == opening:
                bracket_count += 1
            elif word == closing:
                bracket_count -= 1
            if bracket_count <= 0:
                if word != closing:
                    self.word_iter.push_back(word)
                break
            word = self.word_iter.read()

    def __skip_commentary(self):
        word = self.word_iter.read()
        while word is not None and word != "\n":
            word = self.word_iter.read()


def main():
    counter = Counter("../tests/test-07.tex")
    counter.run()
    counter.print_result()


if __name__ == "__main__":
    main()
