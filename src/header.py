class Header:
    """
    Class represents header (all types - title, chapter, section, subsection) and its word counts
    """
    def __init__(self, header_type):
        self.type = header_type  # title, chapter, section, subsection
        self.words = []
        self.header_count = 0
        self.text_count = 0
        self.caption_count = 0

    def add_header_word(self, word):
        self.words.append(word)
        self.header_count += 1

    def add_text_word(self):
        self.text_count += 1

    def add_caption_word(self):
        self.caption_count += 1

    def __str__(self):
        result = "  " + self.type + " ("
        result += str(self.header_count) + " + " + str(self.text_count) + " + " + str(self.caption_count) + ")"
        for word in self.words:
            result += " " + word
        return result
