import counter


def main():
    c = counter.Counter("../tests/test-07.tex")
    c.run()
    c.print_result()

if __name__ == "__main__":
    main()
