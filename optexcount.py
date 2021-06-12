import sys
import os.path
import src.counter


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python3 + " + sys.argv[0] + " path-to-file [-verbose]")
    elif not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + " Invalid filename!")
    elif len(sys.argv) == 3 and sys.argv[2] != "-verbose":
        print(sys.argv[2] + " Invalid specifier!")
    else:
        try:
            if len(sys.argv) == 2:
                c = src.counter.Counter(sys.argv[1])
            else:
                c = src.counter.Counter(sys.argv[1], True)
            c.run()
            c.print_result()
        except Exception as err:
            print()
            print("Problem occurred!")
            print(err)


if __name__ == "__main__":
    main()
