# lexer.py
# Lumen Language - Week 1 Lexer
# Written from scratch (no external libraries)

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Keywords
    LET = auto()
    PRINT = auto()
    IF = auto()

    # Literals & Identifiers
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQ = auto()          # =
    EQEQ = auto()        # ==
    BANGEQ = auto()      # !=
    LT = auto()          # <
    GT = auto()          # >
    LTE = auto()         # <=
    GTE = auto()         # >=

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()

    EOF = auto()
    ILLEGAL = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', line={self.line}, col={self.column})"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_column = 1

        self.keywords = {
            "let": TokenType.LET,
            "print": TokenType.PRINT,
            "if": TokenType.IF,
        }

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected: str) -> bool:
        if self.is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def add_token(self, type: TokenType, lexeme: Optional[str] = None):
        text = lexeme if lexeme is not None else self.source[self.start:self.current]
        self.tokens.append(Token(type, text, self.line, self.start_column))

    def skip_whitespace_and_comments(self):
        while not self.is_at_end():
            c = self.peek()
            if c in (" ", "\t", "\r"):
                self.advance()
            elif c == "\n":
                self.advance()
                self.line += 1
                self.column = 1
            elif c == "/" and self.peek_next() == "/":
                # Line comment
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                break

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
                self.column = 1
            self.advance()

        if self.is_at_end():
            self.add_token(TokenType.ILLEGAL, "Unterminated string")
            return

        self.advance()  # closing "
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        self.add_token(TokenType.NUMBER)

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, TokenType.IDENT)
        self.add_token(token_type)

    def scan_token(self):
        self.skip_whitespace_and_comments()
        self.start = self.current
        self.start_column = self.column

        if self.is_at_end():
            self.add_token(TokenType.EOF)
            return

        c = self.advance()

        if c.isalpha() or c == "_":
            self.identifier()
        elif c.isdigit():
            self.number()
        elif c == '"':
            self.string()
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "/":
            self.add_token(TokenType.SLASH)
        elif c == "(":
            self.add_token(TokenType.LPAREN)
        elif c == ")":
            self.add_token(TokenType.RPAREN)
        elif c == "{":
            self.add_token(TokenType.LBRACE)
        elif c == "}":
            self.add_token(TokenType.RBRACE)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "=":
            if self.match("="):
                self.add_token(TokenType.EQEQ)
            else:
                self.add_token(TokenType.EQ)
        elif c == "!":
            if self.match("="):
                self.add_token(TokenType.BANGEQ)
            else:
                self.add_token(TokenType.ILLEGAL, c)
        elif c == "<":
            if self.match("="):
                self.add_token(TokenType.LTE)
            else:
                self.add_token(TokenType.LT)
        elif c == ">":
            if self.match("="):
                self.add_token(TokenType.GTE)
            else:
                self.add_token(TokenType.GT)
        else:
            self.add_token(TokenType.ILLEGAL, c)

    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.scan_token()
        # Ensure EOF is always present
        if not self.tokens or self.tokens[-1].type != TokenType.EOF:
            self.add_token(TokenType.EOF)
        return self.tokens


# Simple test when run directly
if __name__ == "__main__":
    sample = '''
    let x = 10;
    let name = "Lumen";
    print x + 5 * 2;
    if x > 5 {
        print "yes";
    }
    // this is a comment
    '''
    lexer = Lexer(sample)
    tokens = lexer.tokenize()
    for t in tokens:
        print(t)