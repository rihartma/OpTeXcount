# OpTeXcount

What is OpTeXcount? It is a basic python script that analyzes OpTeX source code and counts words in specific categories. For more information about this tool read `optexcount-doc.pdf`.
### How to use it?
Run: `python3 optexcount.py filename [-verbose] [-set-verbchar=verb-char]`, where `filename` is the name of our OpTeX code file. What does the optional argument `-verbose`? It prints the entire source code with colored words according to their categories. `-set-verbchar=verb-char` sets the implicit inline verbatim character to `verb-char`
