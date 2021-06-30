#!/usr/bin/env python3

"""
The main file for entire optexcount utility
Author: Richard Hartmann
Version: 1.1
"""


import argparse
import counter


def main():
    parser = argparse.ArgumentParser(description="Word counter of OpTeX documents")
    parser.add_argument('filename', help='filename of our OpTeX file', type=argparse.FileType('r'))
    parser.add_argument("-v", "--verbose", help="activate verbose mode", action="store_true")
    parser.add_argument('-s', '--set-verbchar', help='set implicit inline verbatim character', nargs=1)
    parser.add_argument('--version', action='version', version='Version 1.1')
    args = parser.parse_args()
    if args.set_verbchar:
        if len(args.set_verbchar[0]) != 1:
            parser.error("SET_VERBCHAR must be a character")
            raise argparse.ArgumentTypeError("SET_VERBCHAR must be a character")
        else:
            args.set_verbchar = args.set_verbchar[0]

    try:
        c = counter.Counter(args.filename.name, args.verbose, args.set_verbchar)
        c.run()
        c.print_result()
    except Exception as err:
        print()
        print("Problem occurred!")
        print(err)


if __name__ == "__main__":
    main()
