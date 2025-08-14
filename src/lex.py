from enum import Enum
from dataclasses import dataclass


class TokenType(Enum):
    # Constants
    IDENTIFIER = 0
    CONSTANT = 1
    # Keywords
    KW_INT = "int"
    KW_VOID = "void"
    KW_RETURN = "return"
    # Punctuation
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    SEMICOLON = ";"
    TILDE = "~"
    HYPHEN = "-"
    DOUBLE_HYPHEN = "--"


@dataclass
class Token:
    token_type: TokenType
    value: str


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.tokens: list[Token] = []
        self.start = 0
        self.end = len(input)
        self.current = 0

    def is_at_end(self) -> bool:
        return self.current >= self.end

    def lex(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        return self.tokens

    def advance(self) -> str:
        c = self.input[self.current]
        self.current += 1
        return c

    def peek(self) -> str:
        return self.input[self.current]

    def number(self):
        while str.isdecimal(self.peek()):
            self.advance()

        if not self.is_at_end() and str.isalpha(self.peek()):
            raise RuntimeError("Invalid number")

        self.tokens.append(
            Token(TokenType.CONSTANT, self.input[self.start : self.current])
        )

    def identifier(self):
        while str.isalnum(self.peek()):
            self.advance()

        text = self.input[self.start : self.current]

        match text:
            case "int":
                self.tokens.append(Token(TokenType.KW_INT, None))
            case "void":
                self.tokens.append(Token(TokenType.KW_VOID, None))
            case "return":
                self.tokens.append(Token(TokenType.KW_RETURN, None))
            case _:
                self.tokens.append(Token(TokenType.IDENTIFIER, text))

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.tokens.append(Token(TokenType.OPEN_PAREN, None))
            case ")":
                self.tokens.append(Token(TokenType.CLOSE_PAREN, None))
            case "{":
                self.tokens.append(Token(TokenType.OPEN_BRACE, None))
            case "}":
                self.tokens.append(Token(TokenType.CLOSE_BRACE, None))
            case ";":
                self.tokens.append(Token(TokenType.SEMICOLON, None))
            case "~":
                self.tokens.append(Token(TokenType.TILDE, None))
            case "-":
                if self.peek() == "-":
                    self.tokens.append(Token(TokenType.DOUBLE_HYPHEN, None))
                else:
                    self.tokens.append(Token(TokenType.HYPHEN, None))
            case " " | "\t" | "\r" | "\n":
                # Ignore whitespace
                pass
            case _ if c.isnumeric():
                self.number()
            case _ if c.isalpha():
                self.identifier()
            case c:
                raise RuntimeError(f"{c} is not an acceptable character")
