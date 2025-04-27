// tokens.h
#ifndef TOKENS_H
#define TOKENS_H

enum yytokentype {
    IDENTIFIER = 258,
    INTEGER_LITERAL,
    STRING_LITERAL,
    IF, ELSE, WHILE, READ, WRITE,
    INT_TYPE, STRING_TYPE,
    ASSIGN, EQ, LT, LE, GT, GE,
    PLUS, MINUS, MUL, DIV,
    AND, OR, NOT,
    LPAREN, RPAREN, LBRACK, RBRACK, LBRACE, RBRACE,
    COMMA, SEMICOLON,
    INVALID
};

typedef union {
    int intval;
    char* str;
} YYSTYPE;

extern YYSTYPE yylval;

#endif
