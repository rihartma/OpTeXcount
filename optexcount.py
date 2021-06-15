import sys
import os.path
import src.counter


def main():
    if len(sys.argv) < 2 and len(sys.argv) > 4:
        print("Usage: python3 " + sys.argv[0] + " path-to-file [-verbose] [-set-verbchar=verbatim-character]")
    elif not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " Invalid filename!")
    elif len(sys.argv) == 3 and sys.argv[2] != "-verbose" and sys.argv[2][0:-1] != "-set-verbchar=":
        print(sys.argv[2] + " Invalid specifier!")
        print("Usage: python3 " + sys.argv[0] + " path-to-file [-verbose] [-set-verbchar=verbatim-character]")
    elif len(sys.argv) == 4 and sys.argv[2] != "-verbose" and sys.argv[3][0:-1] != "-set-verbchar=":
        if sys.argv[2] != "-verbose":
            print(sys.argv[2] + " Invalid specifier!")
        if sys.argv[3][0:-1] != "-set-verbchar=":
            print(sys.argv[3] + " Invalid specifier!")
        print("Usage: python3 + " + sys.argv[0] + " path-to-file [-verbose] [-set-verbchar=verbatim-character]")
    else:
        verb_char = None
        verbose_mode = False
        if len(sys.argv) == 4:
            verbose_mode = True
            verb_char = sys.argv[3][-1]
        elif len(sys.argv) == 3:
            if sys.argv[2] == "-verbose":
                verbose_mode = True
            else:
                verb_char = sys.argv[2][-1]
        try:
            c = src.counter.Counter(sys.argv[1], verbose_mode, verb_char)
            c.run()
            c.print_result()
        except Exception as err:
            print()
            print("Problem occurred!")
            print(err)


if __name__ == "__main__":
    main()
