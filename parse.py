import sys

from lex import Lexer, Token, TokenType


class Parser:
    """ Parser object keeps track of current token and checks if the code matches the grammar.

    The Grammar
    program ::= {statement}
    statement ::= "PRINT" (expression | string) nl
        | "IF" comparison "THEN" nl {statement} "ENDIF" nl
        | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
        | "LABEL" ident nl
        | "GOTO" ident nl
        | "LET" ident "=" expression nl
        | "INPUT" ident nl
    comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    expression ::= term {( "-" | "+" ) term}
    term ::= unary {( "/" | "*" ) unary}
    unary ::= ["+" | "-"] primary
    primary ::= number | ident
    nl ::= '\n'+

    comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    expression ::= term {( "-" | "+" ) term}
    term ::= unary {( "/" | "*" ) unary}
    unary ::= ["+" | "-"] primary
    primary ::= number | ident
    """

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.symbols = set()  # Variables declared so far.
        self.labels_declared = set()  # Labels declared so far.
        self.labels_gone_to = set()  # Labels goto'ed so far.
        self.current_token: Token = None
        self.peek_token: Token = None
        self.next_token()
        self.next_token()  # Call this twice to initialize current and peek.

    def is_token(self, kind: TokenType) -> bool:
        # Return true if the current token matches.
        return kind == self.current_token.kind

    def is_next_token(self, kind: TokenType) -> bool:
        # Return true if the next token matches.
        return kind == self.peek_token.kind

    def match(self, kind: TokenType) -> None:
        # Try to match current token. If not, error. Advances the current token.
        if not self.is_token(kind):
            self.abort(f"Expected {kind.name}, got {self.current_token.name}")
        self.next_token()

    def next_token(self) -> None:
        # Advances the current token.
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()
        # No need to worry about parsing the EOF. Lexer handles that.

    def abort(self, message: str) -> None:
        sys.exit(f"Error. {message}")

    # Production rules #

    def program(self) -> None:
        # program ::= {statement}
        print("PROGRAM")

        while self.is_token(TokenType.NEWLINE):
            # Since some newlines are required in our grammar, we need to skip the excess.
            self.next_token()

        while not self.is_token(TokenType.EOF):
            # Parse all the statements in the program.
            self.statement()

        for label in self.labels_gone_to:
            # Check that each label referenced in a GOTO is declared.
            if label not in self.labels_declared:
                self.abort(f"Attempting to GOTO to undeclared label: {label}")

    def statement(self) -> None:
        # One of the following statements...

        # Check the first token to see what kind of statement this is.
        if self.is_token(TokenType.PRINT):
            # "PRINT" (expression | string)
            print("STATEMENT-PRINT")
            self.next_token()
            if self.is_token(TokenType.STRING):
                # Simple string.
                self.next_token()
            else:
                # Expect an expression.
                self.expression()

        elif self.is_token(TokenType.IF):
            # "IF" comparison "THEN" {statement} "ENDIF"
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()
            self.match(TokenType.THEN)
            self.nl()
            while not self.is_token(TokenType.ENDIF):
                # Zero or more statements in the body.
                self.statement()
            self.match(TokenType.ENDIF)

        elif self.is_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()
            self.match(TokenType.REPEAT)
            self.nl()
            while not self.is_token(TokenType.ENDWHILE):
                # Zero or more statements in the loop body.
                self.statement()
            self.match(TokenType.ENDWHILE)

        elif self.is_token(TokenType.LABEL):
            # "LABEL" ident
            print("STATEMENT-LABEL")
            self.next_token()
            if self.current_token.text in self.labels_declared:
                # Make sure this label doesn't already exist.
                self.abort(f"Label already exists: {self.current_token.text}")
            self.labels_declared.add(self.current_token.text)
            self.match(TokenType.IDENT)

        elif self.is_token(TokenType.GOTO):
            # "GOTO" ident
            print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gone_to.add(self.current_token.text)
            self.match(TokenType.IDENT)

        elif self.is_token(TokenType.LET):
            # "LET" ident "=" expression
            print("STATEMENT-LET")
            self.next_token()
            if self.current_token.text not in self.symbols:
                # Check if ident exists in symbol table. If not, declare it.
                self.symbols.add(self.current_token.text)
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.is_token(TokenType.INPUT):
            # "INPUT" ident
            print("STATEMENT-INPUT")
            self.next_token()
            if self.current_token.text not in self.symbols:
                # If variable doesn't already exist, declare it.
                self.symbols.add(self.current_token.text)
            self.match(TokenType.IDENT)

        else:
            # This is not a valid statement. Error!
            self.abort(
                f"Invalid statement at {self.current_token.text} ({self.current_token.kind.name})"
            )

        # Newline.
        self.nl()

    def nl(self) -> None:
        # nl ::= '\n'+
        print("NEWLINE")

        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # But we allow extra newlines too.
        while self.is_token(TokenType.NEWLINE):
            self.next_token()

    def comparison(self) -> None:
        # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
        print("COMPARISON")

        self.expression()
        if self.is_comparison_operator():
            # Must be at least one comparison operator and another expression.
            self.next_token()
            self.expression()
        while self.is_comparison_operator():
            # Can have 0 or more comparison operator adn expressions.
            self.next_token()
            self.expression()

    def is_comparison_operator(self) -> bool:
        # Return true if the current token is a comparison operator.
        return (
            self.is_token(TokenType.GT)
            or self.is_token(TokenType.GTEQ)
            or self.is_token(TokenType.LT)
            or self.is_token(TokenType.LTEQ)
            or self.is_token(TokenType.EQEQ)
            or self.is_token(TokenType.NOTEQ)
        )

    def expression(self) -> None:
        # expression ::= term {( "-" | "+" ) term}
        print("EXPRESSION")

        self.term()
        while self.is_token(TokenType.PLUS) or self.is_token(TokenType.MINUS):
            # Can have 0 or more +/- and expressions.
            self.next_token()
            self.term()

    def term(self) -> None:
        # term ::= unary {( "/" | "*" ) unary}
        print("TERM")

        self.unary()
        while self.is_token(TokenType.ASTERISK) or self.is_token(TokenType.SLASH):
            # Can have 0 or more *// and expressions.
            self.next_token()
            self.unary()

    def unary(self) -> None:
        # unary ::= ["+" | "-"] primary
        print("UNARY")

        if self.is_token(TokenType.PLUS) or self.is_token(TokenType.MINUS):
            # Optional unary +/-
            self.next_token()
        self.primary()

    def primary(self):
        # primary ::= number | ident
        print(f"PRIMARY ({self.current_token.text})")

        if self.is_token(TokenType.NUMBER):
            self.next_token()
        elif self.is_token(TokenType.IDENT):
            if self.current_token.text not in self.symbols:
                # Ensure the variable already exists.
                self.abort(
                    f"Referencing variable before assignment: {self.current_token.text}"
                )
            self.next_token()
        else:
            # Error!
            self.abort(f"Unexpected token at {self.current_token.text}")
