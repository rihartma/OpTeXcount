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
    "\\hyperlinks": ["C", "C"],
    "\\outlines": ["C"],
    "\\magscale": ["S"],
    "\\margins": ["O", "W", "P", "W"],
    "\\style": ["W"],
    "\\url": ["C"],
    "\\loadmath": ["C"],
    "\\everytt": ["C"],
    "\\eqmark": ["S"]
}

"""
List of keywords that introduce some floats, we want to be counted in section table/floats/figures
Pay attention! This keyword MUST be introduced in keyword_list too, otherwise it won't count words properly!
"""
floats_keywords = ["\\table", "\\inspic"]

"""
Dictionary of keys - keywords and values - their counts
Keywords(keys) represents macros/aliases that are replaced by certain number of words(values)
"""
aliases = {
    "\TeX": 1,
    "\OpTeX": 1,
    "\LuaTeX": 1,
    "\XeTeX": 1,
    "\OPmac": 1,
    "\CS": 1,
    "\csplain": 1
}