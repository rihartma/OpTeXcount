"""
List of known keywords that has got some arguments
"O" - strOke argument
"W" - argument Without brackets
"S" - argument in Square brackets
"P" - argument in Parentheses
"C" - argument in Curly brackets
"""
keywords_list = {
    "\\ii": ["W", "W"],
    "\\label": ["S"],
    "\\ref": ["S"],
    "\\pgref": ["S"],
    "\\caption": ["0"],
    # "\\verbchar":[],
    "\\begmulti": ["W"],
    "\\cite": ["S"],
    "\\rcite": ["S"],
    "\\bib": ["S"],
    "\\usebib": ["O", "P", "W"],
    "\\load": ["S"],
    "\\fontfam": ["S"],
    "\\typosize": ["S"],
    "\\typoscale": ["S"],
    "\\thefontsize": ["S"],
    "\\thefontscale": ["S"],
    "\\inspic": ["W"],
    "\\table": ["C", "C"],
    # "\\fnote":["C"],
    # "\\mnote":["C"],
    "\\hyperlinks": ["C", "C"],
    "\\outlines": ["C"],
    "\\magscale": ["S"],
    "\\margins": ["O", "W", "P", "W"],
    "\\style": ["W"],
    "\\url": ["C"],
    "\\loadmath": ["C"]
}
