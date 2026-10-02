# parser.py
# Lumen Language - Week 2 Recursive Descent Parser + AST
# Written from scratch (no external libraries)

from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Union
from lexer import Token, TokenType, Lexer


# ==================== AST Node Definitions ====================

@dataclass
class NumberNode:
    value: int

@dataclass
class StringNode:
    value: str

@dataclass
class IdentifierNode:
    name: str

@dataclass
class BinaryOpNode:
    left: object
    op: TokenType
    right: object

@dataclass
class UnaryOpNode:
    op: TokenType
    operand: object

@dataclass
class AssignmentNode:
    name: str
    value: object

@dataclass
class PrintNode:
    expression: object

@dataclass
class IfNode:
    condition: object
    body: List[object]

@dataclass
class ProgramNode:
    statements: List[object]


# ==================== Parser ====================

class ParseError(Exception):
    def __init__(self, message: str, token: Token = None):
        self.message = message
        self.token = token
        super().__init__(self.message)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def match(self, *types: TokenType) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise ParseError(message, self.peek())

    # -------------------- Grammar Rules --------------------

    def parse(self) -> ProgramNode:
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return ProgramNode(statements)

    def statement(self):
        if self.match(TokenType.LET):
            return self.assignment_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        raise ParseError(f"Expected statement, got {self.peek().type.name}", self.peek())

    def assignment_statement(self) -> AssignmentNode:
        name_token = self.consume(TokenType.IDENT, "Expected variable name after 'let'")
        self.consume(TokenType.EQ, "Expected '=' after variable name")
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return AssignmentNode(name_token.lexeme, value)

    def print_statement(self) -> PrintNode:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after print expression")
        return PrintNode(expr)

    def if_statement(self) -> IfNode:
        condition = self.expression()
        self.consume(TokenType.LBRACE, "Expected '{' after if condition")
        body = []
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            body.append(self.statement())
        self.consume(TokenType.RBRACE, "Expected '}' after if body")
        return IfNode(condition, body)

    # -------------------- Expressions (Precedence Climbing) --------------------

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.EQEQ, TokenType.BANGEQ):
            op = self.previous().type
            right = self.comparison()
            expr = BinaryOpNode(expr, op, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.previous().type
            right = self.term()
            expr = BinaryOpNode(expr, op, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.previous().type
            right = self.factor()
            expr = BinaryOpNode(expr, op, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.previous().type
            right = self.unary()
            expr = BinaryOpNode(expr, op, right)
        return expr

    def unary(self):
        if self.match(TokenType.MINUS):
            op = self.previous().type
            operand = self.unary()
            return UnaryOpNode(op, operand)
        return self.primary()

    def primary(self):
        if self.match(TokenType.NUMBER):
            return NumberNode(int(self.previous().lexeme))
        if self.match(TokenType.STRING):
            return StringNode(self.previous().lexeme)
        if self.match(TokenType.IDENT):
            return IdentifierNode(self.previous().lexeme)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        raise ParseError(f"Unexpected token {self.peek().type.name}", self.peek())


# -------------------- Pretty printer for testing --------------------

def print_ast(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, ProgramNode):
        print(f"{prefix}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)
    elif isinstance(node, AssignmentNode):
        print(f"{prefix}Assignment: {node.name} =")
        print_ast(node.value, indent + 1)
    elif isinstance(node, PrintNode):
        print(f"{prefix}Print")
        print_ast(node.expression, indent + 1)
    elif isinstance(node, IfNode):
        print(f"{prefix}If")
        print(f"{prefix}  Condition:")
        print_ast(node.condition, indent + 2)
        print(f"{prefix}  Body:")
        for stmt in node.body:
            print_ast(stmt, indent + 2)
    elif isinstance(node, BinaryOpNode):
        print(f"{prefix}BinaryOp: {node.op.name}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)
    elif isinstance(node, UnaryOpNode):
        print(f"{prefix}UnaryOp: {node.op.name}")
        print_ast(node.operand, indent + 1)
    elif isinstance(node, NumberNode):
        print(f"{prefix}Number: {node.value}")
    elif isinstance(node, StringNode):
        print(f"{prefix}String: \"{node.value}\"")
    elif isinstance(node, IdentifierNode):
        print(f"{prefix}Identifier: {node.name}")
    else:
        print(f"{prefix}Unknown node: {node}")


# Simple test when run directly
if __name__ == "__main__":
    sample = '''
    let x = 10;
    let y = 5;
    print x + y * 2;
    if x > y {
        print "x is bigger";
        let z = x - y;
        print z;
    }
    print "Done";
    '''
    lexer = Lexer(sample)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("=== AST ===")
        print_ast(ast)
        print("\nParser completed successfully.")
    except ParseError as e:
        print(f"Parse error: {e.message}")
        if e.token:
            print(f"  at line {e.token.line}, column {e.token.column}")