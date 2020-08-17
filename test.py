import unittest
import subprocess
from typing import List

from lex import Lexer, TokenType


class TestLexer(unittest.TestCase):
    """ Tests
        Occasionally throughout the compiler tutorial, the author includes
        changes to `main.py` to verify the changes made in the last
        section. Rather than leave these behind every time we expand the
        functionality of the compiler, these make obvious use-case for tests.
    """

    def harness(self, input: str) -> List[TokenType]:
        """ Harness
            The lexer accepts a string of source code as input
            and finds the individual pieces (called tokens)
            that we care about. Since all the test_lexing_* methods
            follow the same pattern, set up a harness to abstract the process.
        """
        output = []
        lexer = Lexer(input)
        token = lexer.get_token()
        while token.kind != TokenType.EOF:
            output.append(token.kind)
            token = lexer.get_token()
        return output

    def test_lexing_tokens(self):
        input = "LET foobar = 123"
        self.assertEqual(
            self.harness(input),
            [
                TokenType.LET,
                TokenType.IDENT,
                TokenType.EQ,
                TokenType.NUMBER,
                TokenType.NEWLINE,
            ],
        )

    def test_lexing_whitespace(self):
        input = "+- */"
        self.assertEqual(
            self.harness(input),
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.ASTERISK,
                TokenType.SLASH,
                TokenType.NEWLINE,
            ],
        )

    def test_lexing_multicharacter_tokens(self):
        input = "+- */ >>= = !="
        self.assertEqual(
            self.harness(input),
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.ASTERISK,
                TokenType.SLASH,
                TokenType.GT,
                TokenType.GTEQ,
                TokenType.EQ,
                TokenType.NOTEQ,
                TokenType.NEWLINE,
            ],
        )

    def test_lexing_comments(self):
        input = "+- # This is a comment!\n */"
        self.assertEqual(
            self.harness(input),
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.NEWLINE,
                TokenType.ASTERISK,
                TokenType.SLASH,
                TokenType.NEWLINE,
            ],
        )

    def test_lexing_comments_and_strings(self):
        input = '+- "This is a string" # This is a comment!\n */'
        self.assertEqual(
            self.harness(input),
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.STRING,
                TokenType.NEWLINE,
                TokenType.ASTERISK,
                TokenType.SLASH,
                TokenType.NEWLINE,
            ],
        )

    def test_lexing_numbers(self):
        input = "+-123 9.8654*/"
        self.assertEqual(
            self.harness(input),
            [
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.NUMBER,
                TokenType.NUMBER,
                TokenType.ASTERISK,
                TokenType.SLASH,
                TokenType.NEWLINE,
            ],
        )

    def lest_lexing_keywords(self):
        input = "IF+-123 foo*THEN/"
        self.assertEqual(
            self.harness(input),
            [
                TokenType.IF,
                TokenType.PLUS,
                TokenType.MINUS,
                TokenType.NUMBER,
                TokenType.IDENT,
                TokenType.ASTERISK,
                TokenType.THEN,
                TokenType.SLASH,
                TokenType.NEWLINE,
            ],
        )


class TestEmitter(unittest.TestCase):
    """ Testing the Emitter
    """

    def harness(self, name: str):
        tiny = f"{name}.tiny"
        c = f"{name}.c"
        subprocess.run(["python3", "main.py", tiny])
        with open("out.c", "r") as resulting_file:
            output = resulting_file.read()
        with open(c, "r") as reference_file:
            reference = reference_file.read()
        return output, reference

    def test_statements(self):
        input_file, output_file = self.harness("statements")
        self.assertEqual(input_file, output_file)

    def test_fibonacci(self):
        input_file, output_file = self.harness("fibonacci")
        self.assertEqual(input_file, output_file)

    def test_average(self):
        input_file, output_file = self.harness("average")
        self.assertEqual(input_file, output_file)


if __name__ == "__main__":
    unittest.main()
