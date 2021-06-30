import keywords as kw
import word_iterator as wi
import header as hd
import color_print as cp


class Counter:
    """
    Class that analyzes a source code and counts word counts
    """

    def __init__(self, filename, color_print=False, verb_char=None):
        self.word_iter = wi.WordIterator(filename)  # source of words that will be analyzed
        if verb_char is not None:
            self.word_iter.add_separator(verb_char)
        self.verb_char = verb_char  # used for inline verbatim text
        self.color_print = color_print  # input text will be printed(with colors)
        self.printer = cp.Printer()
        self.regular_words_count = 0
        self.header_words_count = 0
        self.caption_words_count = 0
        self.figure_float_count = 0
        self.math_inline_count = 0
        self.math_count = 0
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
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "\\bye":
            self.__process_word(pair)
            pair = self.word_iter.read()
        if pair is not None:
            self.print_keyword(pair)
            self.print_irrelevant_word(("", "\n"))

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

    def print_counted_word(self, pair):
        """
        Prints word that was counted. The color depends on category of the word.
        """
        if not self.color_print:
            return
        if self.__context == "regular-text":
            self.printer.blue(pair[0]+pair[1])
        elif self.__context == "header":
            self.printer.cyan(pair[0]+pair[1])
        elif self.__context == "caption":
            self.printer.green(pair[0]+pair[1])

    def print_keyword(self, pair):
        """
        Prints keyword - word with red color
        """
        if not self.color_print:
            return
        self.printer.red(pair[0]+pair[1])

    def print_irrelevant_word(self, pair):
        """
        Prints words that wasn't counted and are not important for our functionality, like commentary words etc...
        """
        if not self.color_print:
            return
        self.printer.white(pair[0]+pair[1])

    def __process_word(self, pair):
        """
        Decides how to treat with word from argument
        """
        if len(pair[0]) == 0 or pair[0] == "\n":  # empty word or newline
            self.print_irrelevant_word(pair)
        elif pair[0] == "%":
            self.print_irrelevant_word(pair)
            self.__skip_commentary()
        elif pair[0] == "{":
            self.print_irrelevant_word(pair)
            self.__load_curly_brackets()
        elif pair[0] == "$":
            self.print_keyword(pair)
            self.__load_inline_formulae()
        elif pair[0] == "$$":
            self.print_keyword(pair)
            self.__load_formulae()
        elif self.verb_char is not None and pair[0] == self.verb_char:
            self.print_keyword(pair)
            self.__load_verbatim(self.verb_char)
        elif self.__is_keyword(pair[0]):
            self.__process_keyword(pair)
        else:
            self.__process_text_word(pair)

    def __process_keyword(self, pair):
        """
        Treats with keywords.
        Calls action on known keywords that are important for the counter
        If keyword is unknown it is skipped
        """
        word, arg = self.__split_keyword(pair[0])
        self.print_keyword((word, ''))
        if arg is None:
            self.print_irrelevant_word(('', pair[1]))
        else:
            self.print_irrelevant_word((arg, pair[1]))
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
            self.__skip_commentary()
            self.__load_verbatim()
        elif word == '\\verbchar' or word == '\\activettchar':  # keywords with same functionality
            self.__set_verb_char(word, arg, pair[1])
        elif word == '\\code':
            self.__load_code_verbatim()
        elif word in kw.logos:
            self.__load_logo(word, arg, pair[1])
        else:
            pass  # skip unknown keywords

    def __process_text_word(self, pair):
        """
        Increases word counts based on the word location - word context
        """
        # word with only one character that is not alphanumeric won't be counted as word
        if len(pair[0]) == 0:
            self.print_irrelevant_word(pair)
        elif len(pair[0]) == 1 and not pair[0].isalnum():
            self.print_irrelevant_word(pair)
        elif self.__context == "regular-text":
            self.print_counted_word(pair)
            self.regular_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_text_word()
        elif self.__context == "header":
            self.print_counted_word(pair)
            self.header_words_count += 1
            self.all_headers[-1].add_header_word(pair[0])
        elif self.__context == "caption":
            self.print_counted_word(pair)
            self.caption_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_caption_word()

    @staticmethod
    def __is_keyword(word):
        """
        Decides whether word is keyword or not
        """
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
        pair = self.word_iter.read()
        skip_new_line = False
        while pair is not None and pair[0] != "\\bye":
            if not len(pair[0]):
                self.print_irrelevant_word(pair)
            elif pair[0] == "\n":
                self.print_irrelevant_word(pair)
                if not skip_new_line:
                    self.__context = orig_context
                    return
                skip_new_line = False
            elif pair[0] == "^^J":
                self.print_irrelevant_word(pair)
                skip_new_line = True
            else:
                self.__process_word(pair)
                skip_new_line = False
            pair = self.word_iter.read()
        self.__context = orig_context
        if pair is not None:
            self.__process_keyword(pair)

    def __load_list(self):
        """
        Loads list - words that are surrounded by '\begitems' and '\enditems'
        """
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "\\enditems":
            if pair[0] != "*":
                self.__process_word(pair)
            else:
                self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        if pair is None:
            raise Exception("No list ending found - \\enditems")
        else:
            self.print_keyword(pair)

    def __load_caption(self):
        """
        Loads caption - words until EOL
        """
        orig_context = self.__context
        self.__context = 'caption'
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "\\bye":
            if pair[0] == "\n":
                self.print_irrelevant_word(pair)
                self.__context = orig_context
                return
            else:
                self.__process_word(pair)
            pair = self.word_iter.read()
        self.__context = orig_context
        if pair is not None:
            self.print_keyword(pair)

    def __load_footnote(self):
        """
        Loads footnote(block in curly brackets)
        """
        orig_context = self.__context
        self.__context = 'caption'
        pair = self.word_iter.read()
        if pair is None:
            raise Exception("No opening curly bracket found!")
        while len(pair[0]) == 0 or pair[0].isspace():
            self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        if pair[0] != "{":
            self.__context = orig_context
            self.word_iter.push_back(pair)
            return
        self.print_irrelevant_word(pair)
        self.__load_curly_brackets()
        self.__context = orig_context

    def __load_formulae(self):
        """
        Loads math formulae($$ as separator)
        """
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "$$":
            self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        if pair is None:
            raise Exception("No end of math formulae found!")
        else:
            self.print_keyword(pair)
        self.math_count += 1

    def __load_inline_formulae(self):
        """
        Loads inline math formulae($ as separator)
        """
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "$":
            self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        self.math_inline_count += 1
        if pair is None:
            raise Exception("No end of inline math formulae found!")
        else:
            self.print_keyword(pair)

    def __load_verbatim(self, ending="\\endtt", keyword_print=True):
        """
        Reads words until ending(param) word occurs.
        These words are processed as regular word(not keywords etc...)
        """
        pair = self.word_iter.read()
        while pair is not None and ending != pair[0]:
            self.__process_text_word(pair)
            pair = self.word_iter.read()
        if pair is None:
            raise Exception("Verbatim text not terminated!")
        else:
            if keyword_print:
                self.print_keyword(pair)
            else:
                self.print_irrelevant_word(pair)

    def __load_code_verbatim(self):
        """
        In case of verbatim using "\code" keyword
        """
        pair = self.word_iter.read()
        while len(pair[0]) == 0 or pair[0].isspace():
            self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        if pair[0] != "{":
            raise Exception("\\Code must be followed be opening curly bracket('{')!")
        self.print_irrelevant_word(pair)
        self.__load_verbatim("}", False)

    def __load_logo(self, logo, arg, sep):
        """
        Checks whether logo keyword is followed by slash etc...
        """
        if arg != '/' or len(sep) > 0:
            pass
        elif self.__context == "regular-text":
            self.regular_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_text_word()
        elif self.__context == "header":
            self.header_words_count += 1
            self.all_headers[-1].add_header_word(logo)
        elif self.__context == "caption":
            self.caption_words_count += 1
            if len(self.all_headers):
                self.all_headers[-1].add_caption_word()

    def __set_verb_char(self, word, arg, sep):
        """
        Loads new character for inline verbatim
        """
        if arg is not None and len(arg) == 1:
            self.verb_char = arg
            self.word_iter.add_separator(arg)
        elif arg is None and sep == '':
            pair = self.word_iter.read()
            if len(pair[0]) != 1:
                raise Exception("Invalid use of " + word)
            else:
                self.print_irrelevant_word(pair)
                self.verb_char = pair[0]
                self.word_iter.add_separator(pair[0])
        else:
            raise Exception("Invalid use of " + word)

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
        pair = self.word_iter.read()
        if pair is None or pair[0] == "\\bye":
            raise Exception("No obligatory argument found")
        self.print_irrelevant_word(pair)
        return pair

    def __load_curly_brackets(self):
        """
        Loads block of source code in curly brackets
        """
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "}":
            self.__process_word(pair)
            pair = self.word_iter.read()
        if pair is None:
            raise Exception("No closing bracket ('}') found.")
        else:
            self.print_irrelevant_word(pair)

    def __skip_brackets(self, opening, closing):
        """
        Skips block of source code in brackets opening-closing
        """
        pair = self.word_iter.read()
        bracket_count = 0
        while True:
            if pair is None:
                raise Exception("No closing bracket ('" + closing + "') found.")
            elif pair[0] == opening:
                bracket_count += 1
                self.print_irrelevant_word(pair)
            elif pair[0] == closing:
                bracket_count -= 1
                self.print_irrelevant_word(pair)
            if bracket_count <= 0:
                if pair[0] != closing:
                    self.word_iter.push_back(pair)
                break
            elif pair[0] != opening and pair[0] != closing:
                self.print_irrelevant_word(pair)
            pair = self.word_iter.read()

    def __skip_commentary(self):
        """
        Skips entire line
        """
        pair = self.word_iter.read()
        while pair is not None and pair[0] != "\n":
            self.print_irrelevant_word(pair)
            pair = self.word_iter.read()
        self.print_irrelevant_word(pair)
