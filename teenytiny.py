import sys

from lex import Lexer
from parse import Parser


def main():
    print("Teeny Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], "r") as input_file:
        input_contents = input_file.read()

    # Initialize the lexer and parser.
    lexer = Lexer(input_contents)
    parser = Parser(lexer)

    # Start the parser.
    parser.program()
    print("Parsing complete.")


if __name__ == "__main__":
    main()
