# TeXcount for optex

This script is supposed to analyze source code written in OpTeX.

The code is analyzed and splitted into these 6 categories:
1. Text words
2. Header words
3. Caption words
4. Header Count
5. Figure/Float count
6. Inline formulae
7. Displayed formulae

The functionality is not exactly thought through yet.

### Basic working principle:
Using python script and its library (re) for regular expresions we find in the text key words. Every of this keyword has got its own cathegory. Than we count the words. Later on we might mark up these words in different colors to seperate differente cathegories.
After this analysis we print out the statistics of a particular source code
