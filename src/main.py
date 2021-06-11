import counter
import color_print

# TODO add tex macros representing logos such as \TeX \LaTeX etc...


def main():
    c = counter.Counter("../tests/main_test.tex", True)
    c.run()
    c.print_result()

if __name__ == "__main__":
    main()
