# OpTeXcount

What is OpTeXcount? It is a basic python script that analyzes OpTeX source code and counts words in specific categories. For more information about this tool read `optexcount-doc.pdf`.
### How to install OpTeXcount?
Run: `sudo ./install.sh`
### Usage
Run: `optexcount [-h] [-v] [-s SET_VERBCHAR] [--version] filename`, where `filename` is the name of our OpTeX code file. What does the optional argument `-v/--verbose`? It prints the entire source code with colored words according to their categories. `-s SET_VERBCHAR` or `--set-verbchar SET_VERBCHAR` sets the implicit inline verbatim character to `SET_VERBCHAR` character.
