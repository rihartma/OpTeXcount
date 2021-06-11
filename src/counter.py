import keywords as kw
import word_iterator as wi
import header as hd


class Counter:
    """
    Class that analyzes a source code and counts word counts
    """

    def __init__(self, filename):
        self.word_iter = wi.WordIterator(filename)  # source of words that will be analyzed
        self.regular_words_count = 0
        self.header_words_count = 0
        self.caption_words_count = 0
        self.figure_float_count = 0
        self.math_inline_count = 0
        self.math_count = 0
        self.verb_char = None  # used for inline verbatim text
        self.all_headers = []
        """
        Three possible types of __context:
        1) regular-text (implicit)
        2) headers
        3) captions
        """
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
        elif self.verb_char is not None and word == self.verb_char:
            self.__load_verbatim(self.verb_char)
        elif self.__is_keyword(word):
            self.__process_keyword(word)
        else:
            self.__process_text_word(word)

    def __process_keyword(self, word):
        word, arg = self.__split_keyword(word)
        if word == '\\tit':
            self.all_headers.append(hd.Header("title"))
            self.__load_header()
        elif word == '\\chap':
            self.all_headers.append(hd.Header("chapter"))
            self.__skip_brackets("[", "]")
            self.__load_header()
        elif word == '\\sec':
            self.all_headers.append(hd.Header("section"))
            self.__skip_brackets("[", "]")
            self.__load_header()
        elif word == '\\secc':
            self.all_headers.append(hd.Header("subsection"))
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
            if word in kw.floats_keywords:
                self.figure_float_count += 1
            self.__read_arguments(word)
        elif word == '\\begtt':
            self.__load_verbatim()
        elif word == '\\verbchar' or word == '\\activettchar':  # keywords with same functionality
            self.verb_char = arg
            self.word_iter.add_separator(arg)
        elif word == '\\code':
            self.__load_code_verbatim()
        else:
            pass
            # skip unknown keywords

    def __process_text_word(self, word):
        # all word with only one character that is not alphanumeric won't be counted as word
        if len(word) == 1 and not word.isalnum():
            return
        if self.__context == "regular-text":
            self.regular_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_text_word()
        elif self.__context == "header":
            self.header_words_count += 1
            self.all_headers[-1].add_header_word(word)
        elif self.__context == "caption":
            self.caption_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_caption_word()

    @staticmethod
    def __is_keyword(word):
        if len(word) >= 3:
            if word[0] == '\\' and word[1].isalpha() and word[2].isalpha():
                return True
        return False

    @staticmethod
    def __split_keyword(word):
        """
        Splits word to two part - keyword and its argument
        For example:
        '\verbchar"' will be splitted into pair: '\verbchar', '"'
        """
        for i in range(1, len(word)):
            if not word[i].isalpha():
                return word[:i], word[i:]
        return word, None

    def __load_header(self):
        """
        Loads header
        It reads the source code until new line occurs.
        In case of ^^J at the end of the line it reads until next new line occurs.
        """
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
        """
        Loads list - words that are surrounded by '\begitems' and '\enditems'
        """
        word = self.word_iter.read()
        while word != "\\enditems":
            if word is None:
                raise Exception("No list ending found - \\enditems")
            if word != "*":
                self.__process_word(word)
            word = self.word_iter.read()

    def __load_caption(self):
        """
        Loads caption - words until EOL
        """
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
        """
        Loads footnote(block in curly brackets)
        """
        orig_context = self.__context
        self.__context = 'caption'
        if self.word_iter.read() != "{":
            self.__context = orig_context
            return
        self.__load_curly_brackets()
        self.__context = orig_context

    def __load_formulae(self):
        """
        Loads math formulae($$ as separator)
        """
        word = self.word_iter.read()
        while word != "$$":
            if word is None:
                raise Exception("No end of math formulae found!")
            word = self.word_iter.read()
        self.math_count += 1

    def __load_inline_formulae(self):
        """
        Loads inline math formulae($ as separator)
        """
        word = self.word_iter.read()
        while word != "$":
            if word is None:
                raise Exception("No end of inline math formulae found!")
            word = self.word_iter.read()
        self.math_inline_count += 1

    def __load_verbatim(self, ending="\\endtt"):
        """
        Reads words until ending(param) word occurs.
        These words are processed as regular word(not keywords etc...)
        """
        word = self.word_iter.read()
        while ending != word:
            if word is None:
                raise Exception("Verbatim text not terminated!")
            self.__process_text_word(word)
            word = self.word_iter.read()

    def __load_code_verbatim(self):
        """
        In case of verbatim using "\code" keyword
        """
        word = self.word_iter.read()
        if word != "{":
            raise Exception("\\Code must be followed be opening curly bracket('{')!")
        self.__load_verbatim("}")

    def __read_arguments(self, word):
        """
        Loads from keywords file what arguments has got particular keyword from argument
        These arguments are skipped - not important for our purpose
        """
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
        """
        Just reads another word. In case of the end of source file Exception is thrown
        """
        word = self.word_iter.read()
        if word is None or word == "\\bye":
            raise Exception("No obligatory argument found")
        return word

    def __load_curly_brackets(self):
        """
        Loads block of source code in curly brackets
        """
        word = self.word_iter.read()
        while word != "}":
            if word is None:
                raise Exception("No closing bracket ('}') found.")
            self.__process_word(word)
            word = self.word_iter.read()

    def __skip_brackets(self, opening, closing):
        """
        Skips block of source code in brackets opening-closing
        """
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
        """
        Skips entire line
        """
        word = self.word_iter.read()
        while word is not None and word != "\n":
            word = self.word_iter.read()
