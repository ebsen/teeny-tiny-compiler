import lexer as l


def main():
    input = "IF+-123 foo*THEN/"
    lexer = l.Lexer(input)
    token = lexer.get_token()
    while token.kind != l.TokenType.EOF:
        print(token.kind)
        token = lexer.get_token()


if __name__ == "__main__":
    main()
