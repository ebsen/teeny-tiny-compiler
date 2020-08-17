import sys

from emit import Emitter
from lex import Lexer
from parse import Parser


def main():
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], "r") as input_file:
        input_contents = input_file.read()

    # Initialize the emitter, lexer and parser.
    emitter = Emitter("out.c")
    lexer = Lexer(input_contents)
    parser = Parser(lexer, emitter)

    parser.program()  # Start the parser.
    emitter.write()  # Write the output to file.


if __name__ == "__main__":
    main()
