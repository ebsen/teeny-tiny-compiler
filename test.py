import unittest
from lex import Lexer
from parse import Parser


class TestSuite(unittest.TestCase):
    """ Tests
        Occasionally throughout the compiler tutorial, the author includes
        changes to `teenytiny.py` to verify the changes made in the last
        section. Rather than leave these behind every time we expand the
        functionality of the compiler, these make obvious use-case for tests.
    """

    # inputs = ["LET foobar = 123"]

    def test_the_first(self):
        input = "LET foobar = 123"
        output = ""
        lexer = Lexer(input)
        while lexer.peek() != "\0":
            output += lexer.current_char
            lexer.next_char()
        self.assertEqual(output, input, f"Output should match '{input}'")

    # def test_harness(self):
    #     for input in inputs:


if __name__ == "__main__":
    unittest.main()
