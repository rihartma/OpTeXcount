import re


class WordIterator:
    """
    A basic wrapper for sequential reading of words from file
    """

    def __init__(self, filename):
        self.filename = filename
        self.word_queue = []
        self.line_payload = 50  # how many lines will be loaded into the queue at one time
        self.__lines_count = sum(1 for line in open(filename))
        self.__load_line = 1  # index of first line which haven't been already loaded into the queue
        self.__separators = []

    def read(self):
        """
        Returns first word from file that wasn't already read by this particular object.
        Return value format: (word, separator)
        When all words had been read, it returns None
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

    def add_separator(self, sep):
        """
        All words will be separated with sep separator
        """
        if sep in self.__separators:
            return
        self.__separators.append(sep)
        new_queue = []
        regex_arg = re.compile('(' + sep + ')')
        for word, sep in self.word_queue:
            new_word = re.sub(regex_arg, r' \1 ', word)
            new_words = new_word.split(' ')
            new_queue += self.__make_pairs(word + sep, new_words)
        self.word_queue = new_queue

    def __load_payload(self):
        """
        Loads words from input file into the queue
        Format of words: (word, separator)
        """
        index = 0
        with open(self.filename, 'r') as file:
            for line in file:
                index += 1
                if index < self.__load_line:
                    continue
                elif index < self.__load_line + self.line_payload:
                    self.word_queue += self.__parse_words(line)
                    if index >= self.__lines_count:
                        index += 1
                else:
                    break
        self.__load_line = index

    def __parse_words(self, line):
        """
        Parses a line passed by argument using regular expressions.
        It separates each word on the line and stores it into list.
        returns list of tuples (word, separator between word and next word)
        """
        orig_line = line
        if line == "\n" or line == "\r\n":
            return self.__make_pairs(orig_line, [line])
        # All non escape occurrences of some characters are seperated to be a single 'word'
        line = re.sub(r'(?<!\\)(?:\\\\)*([{}\[\]()%])', r' \1 ', line)
        # $$ and $ are separated from the text to be a single 'word'
        line = re.sub(r'(?<!\\)(?:\\\\)*((\$\$)|(\$))', r' \1 ', line)
        # All escaped alphabetic characters are separated from the previous word
        line = re.sub(r'(?<!\\)(\\\\)*(\\)([A-Za-z])', r'\1 \2\3', line)
        # Non escaped character ~ is replaced with space
        line = re.sub(r'(?<!\\)(?:\\\\)*(~)', r' \1 ', line)
        # Iterate through every separator and put spaces around them
        for sep in self.__separators:
            line = re.sub('(' + sep + ')', r' \1 ', line)
        words_on_line = re.split(r'\s+', line)
        # At the end of every nonempty line newline character is placed
        words_on_line.append("\n")
        return self.__make_pairs(orig_line, words_on_line)

    @staticmethod
    def __make_pairs(orig_line, words):
        """
        Generates list of tuples (word, separator between the word and the next word in list)
        """
        pairs = []
        read_index = 0
        for i in range(len(words)):
            if i + 1 >= len(words):
                start = orig_line[read_index:].find(words[i]) + len(words[i]) + read_index
                pairs.append((words[i], orig_line[start:]))
            else:
                start = orig_line[read_index:].find(words[i]) + len(words[i]) + read_index
                end = orig_line[start:].find(words[i+1]) + start
                pairs.append((words[i], orig_line[start: end]))
                read_index = end
        return pairs
