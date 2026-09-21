# Lumen Language Specification

**Author:Emmanuel Ayibadoubra Yekwe**
**Course:Survey of Programming Languages** 
**University:Niger Delta University**  
**Language Name:Lumen**  
**File Extension:** `.lum`

## 1. Language Philosophy
Lumen is a minimal, Turing-incomplete toy language designed for teaching interpreters.  
It supports variables, arithmetic expressions with proper precedence, string literals, printing, and simple conditional statements.  
There are no loops or recursive constructs, guaranteeing Turing-incompleteness.

## 2. Example Programs

### Example 1 – Basic arithmetic and variables
let x = 10;
let y = 5;
print x + y * 2;

### Example 2 – Strings and concatenation-style usage
let name = "Niger Delta";
print name;
print "Hello " + name;

### Example 3 – Simple conditional
let score = 85;
if score > 50 {
print "Passed";
}
print "Done";

### Example 4 – Nested expressions and parentheses
let a = 4;
let b = 3;
print (a + b) * (a - b);

### Example 5 – Multiple statements
let n = 7;
print n;
let m = n * 2 + 1;
print m;
if m > 10 {
print "Big number";
}

## 3. Formal Grammar (EBNF)
program      ::= statement*
statement    ::= assignment
| print_stmt
| if_stmt
assignment   ::= "let" IDENT "=" expression ";"
print_stmt   ::= "print" expression ";"
if_stmt      ::= "if" expression "{" statement* "}"
expression   ::= term (("+" | "-") term)*
term         ::= factor (("" | "/") factor)
factor       ::= NUMBER
| STRING
| IDENT
| "(" expression ")"
| comparison
comparison   ::= expression (("==" | "!=" | "<" | ">" | "<=" | ">=") expression)?
(* Lexical tokens )
IDENT        ::= letter (letter | digit | "_")
NUMBER       ::= digit+
STRING       ::= '"' [^"]* '"'

## 4. Token Types (for the Lexer)
- `LET`, `PRINT`, `IF`          – keywords
- `IDENT`                       – variable names
- `NUMBER`                      – integer literals
- `STRING`                      – string literals
- `PLUS`, `MINUS`, `STAR`, `SLASH`
- `EQ`, `EQEQ`, `BANGEQ`, `LT`, `GT`, `LTE`, `GTE`
- `LPAREN`, `RPAREN`, `LBRACE`, `RBRACE`
- `SEMICOLON`
- `EOF`

## 5. Notes
- Whitespace and newlines are ignored.
- Line comments start with `//` and continue to the end of the line.
- The language is case-sensitive.
- Only integers and strings are supported as values in Week 1–3.

