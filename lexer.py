import enum
import sys


class Lexer:
    def __init__(self, input):
        # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.source = input + "\n"
        # Added myself so we don't need to keep calling len() all the time.
        self.len = len(self.source)
        # Current character in the string.
        self.current_char = ""
        # Current position in the string.
        self.current_position = -1
        self.next_char()

    def next_char(self):
        # Process the next character.
        self.current_position += 1
        if self.current_position >= self.len:
            self.current_char = "\0"  # EOF
        else:
            self.current_char = self.source[self.current_position]

    def peek(self):
        # Return the lookahead character.
        if self.current_position + 1 >= self.len:
            return "\0"
        return self.source[self.current_position + 1]

    def abort(self, message):
        # Invalid token found, print error message and exit.
        sys.exit(f"Lexing error. {message}")

    def skip_whitespace(self):
        # Skip whitespace except newlines, which we will use to indicate the end of a statement.
        while self.current_char in [" ", "\t", "\r"]:
            self.next_char()

    def skip_comment(self):
        # Skip comments in the code.
        if self.current_char == "#":
            while self.current_char != "\n":
                self.next_char()

    def get_token(self):
        # Return the next token.
        self.skip_whitespace()
        self.skip_comment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., `!=`), number, identifier, or keyword, then we process the rest.
        if self.current_char == "+":
            token = Token(self.current_char, TokenType.PLUS)
        elif self.current_char == "-":
            token = Token(self.current_char, TokenType.MINUS)
        elif self.current_char == "*":
            token = Token(self.current_char, TokenType.ASTERISK)
        elif self.current_char == "/":
            token = Token(self.current_char, TokenType.SLASH)
        elif self.current_char == "=":
            # Check whether this token is `=` or `==`
            if self.peek() == "=":
                prev_char = self.current_char
                self.next_char()
                token = Token(prev_char + self.current_char, TokenType.EQEQ)
            else:
                token = Token(self.current_char, TokenType.EQ)
        elif self.current_char == ">":
            # Check whether this is token is `>` or `>=`
            if self.peek() == "=":
                prev_char = self.current_char
                self.next_char()
                token = Token(prev_char + self.current_char, TokenType.GTEQ)
            else:
                token = Token(self.current_char, TokenType.GT)
        elif self.current_char == "<":
            # Check whether this is token is < or <=
            if self.peek() == "=":
                prev_char = self.current_char
                self.next_char()
                token = Token(prev_char + self.current_char, TokenType.LTEQ)
            else:
                token = Token(self.current_char, TokenType.LT)
        elif self.current_char == '"':
            # Get characters between quotations.
            self.next_char()
            starting_position = self.current_position
            while self.current_char != '"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %
                # We'll be using C's `printf` on this guy.
                if (
                    self.current_char == "\r"
                    or self.current_char == "\n"
                    or self.current_char == "\t"
                    or self.current_char == "\\"
                    or self.current_char == "%"
                ):
                    self.abort("Illegal character in string.")
                self.next_char()
            # Get the substring.
            token_text = self.source[starting_position : self.current_position]
            token = Token(token_text, TokenType.STRING)
        elif self.current_char.isdigit():
            # Leading character is a digit, so this must be a number.
            # Get all consecutive digits and decimal if there is one.
            starting_position = self.current_position
            while self.peek().isdigit():
                self.next_char()
            if self.peek() == ".":
                # Decimal!
                self.next_char()
                # Must have at least one digit after the decimal.
                if not self.peek().isdigit():
                    self.abort("Illegal character in number.")
                while self.peek().isdigit():
                    self.next_char()
            # Get the substring.
            token_text = self.source[starting_position : self.current_position + 1]
            token = Token(token_text, TokenType.NUMBER)
        elif self.current_char.isalpha():
            # Leading character is a letter, so this must be an identifier or a keyword.
            # Get all consecutive alpha numberic characters.
            starting_position = self.current_position
            while self.peek().isalnum():
                self.next_char()
            # Check if the token is in the list of keywords
            token_text = self.source[
                starting_position : self.current_position + 1
            ]  # Get the substring.
            keyword = Token.check_if_keyword(token_text)
            if keyword == None:
                # Identifier
                token = Token(token_text, TokenType.IDENT)
            else:
                # Keyword
                token = Token(token_text, keyword)
        elif self.current_char == "!":
            if self.peek() == "=":
                prev_char = self.current_char
                self.next_char()
                token = Token(prev_char + self.current_char, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.current_char == "\n":
            token = Token(self.current_char, TokenType.NEWLINE)
        elif self.current_char == "\0":
            token = Token(self.current_char, TokenType.EOF)
        else:
            # Unknown token!
            self.abort(f"Unknown token: {self.current_char}")
        self.next_char()
        return token


class Token:
    # Contains the original text and the types of token
    def __init__(self, text, kind):
        # The token's actual text. Used for identifiers, strings, and numbers.
        self.text = text
        # The TokenType that this token is classified as.
        self.kind = kind

    @staticmethod
    def check_if_keyword(text):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            # if kind.name == text and kind.value >= 100 and kind.value < 200:
            if kind.name == text and (100 <= kind.value < 200):
                return kind
        return None


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
