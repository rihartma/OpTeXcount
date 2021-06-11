import counter

# TODO add tex macros representing logos such as \TeX \LaTeX etc...


def main():
    c = counter.Counter("../tests/main_test.tex")
    c.run()
    c.print_result()

if __name__ == "__main__":
    main()
