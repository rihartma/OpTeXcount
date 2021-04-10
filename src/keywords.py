"""

We will divide the keywords into sections representing their functionality.

Sections id & description:

2   Headers - keywords in this section representing keywords that are used to
    introduce titel, chapter, section etc... It has got specific behaviour. It
    is terminated by end of line

3   Captions - keywords that are used to describe tables, images etc...

6   Inline formulae - they are generally introduced with $ ... $

7   Displayed formulae - they are generally introduces with $$ ... $$

------------------------------------------------------------------------------
Note: all keywords in particular sections should behave in same way

"""

# section 2 keywords
headers = ["\\tit", "\\chap", "\\sec", "\\secc"]

# section 3 keywords
captions = ["\\caption/t", "\\caption/f"]

# section 6
# ---

#section 7
# ---


"""
In the script keywords are used using disctionary because of efficient searching
structure: { key - keyword: value - id of section }
"""
key_words = {}

def initialize ():

    for h in headers:
        key_words [h] = 2

    for c in captions:
        key_words [c] = 3