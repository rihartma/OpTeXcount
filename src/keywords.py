

#headers = ["\\tit", "\\chap", "\\sec", "\\secc"]
# blank_keywords = ["\\nl", "\\bye", "\\Blue", "\\Red", "\\Brown", "\\Green", "\\Yellow", "\\Cyan", "\\Magenta", "\\White", "\\Grey", "\\LightGreyand", "\\Black", "\\chyph"]


'''
List of known keywords with their arguments
empty list - no argument
"B" - obligatory arguments
"O" - optional arguments

'''
all_keywords = {
    "\\tit":[],
    "\\chap":[],
    "\\sec":[],
    "\\secc":[],
    "\\maketoc":[],
    "\\ii":[],
    "\\makeindex":[],
    "\\label":[],
    "\\ref":[],
    "\\pgref":[],
    "\\caption/t":[],
    "\\caption/f":[],
    "\\eqmark":[],
    "\\begitems":[],
    "\\enditems":[],
    "\\begblock":[],
    "\\endblock":[],
    "\\begtt":[],
    "\\endtt":[],
    "\\verbchar":[],
    "\\code":[],
    "\\verbinput":[],
    "\\begmulti":[],
    "\\endmulti":[],
    "\\cite":[],
    "\\rcite":[],
    "\\sortcitations":[],
    "\\shortcitations":[],
    "\\nonumcitations":[],
    "\\bib":[],
    "\\usebib":[],
    "\\load":[],
    "\\fontfam":["O"],
    "\\typosize":["O"],
    "\\typoscale":[],
    "\\thefontsize":[],
    "\\thefontscale":[],
    "\\inspic":[],
    "\\table":[],
    "\\fnote":[],
    "\\mnote":[],
    "\\hyperlinks":[],
    "\\outlines":[],
    "\\magscale":[],
    "\\margins":[],
    "\\report":[],
    "\\letter":[],
    "\\slides":[],
    "\\chyph":[],
    "\\style":["B"],
    "\\novspace":[]
}

# def initialize ():

#     for h in headers:
#         key_words [h] = headers

#initialize()