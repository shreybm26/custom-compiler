%{
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "tokens.h"

FILE* token_out;
%}

digit       [0-9]
letter      [a-zA-Z]
id          {letter}({letter}|{digit})*
int_lit     {digit}+
str_lit     \"[^\"]*\"

%%

"if"            { fprintf(token_out, "IF\n"); }
"else"          { fprintf(token_out, "ELSE\n"); }
"while"         { fprintf(token_out, "WHILE\n"); }
"read"          { fprintf(token_out, "READ\n"); }
"write"         { fprintf(token_out, "WRITE\n"); }
"int"           { fprintf(token_out, "INT_TYPE\n"); }
"string"        { fprintf(token_out, "STRING_TYPE\n"); }
"and"           { fprintf(token_out, "AND\n"); }
"or"            { fprintf(token_out, "OR\n"); }
"not"           { fprintf(token_out, "NOT\n"); }

{id} {
    char buffer[33];
    snprintf(buffer, 33, "%s", yytext);
    for (int i = 0; buffer[i]; i++) buffer[i] = tolower(buffer[i]);
    fprintf(token_out, "IDENTIFIER %s\n", buffer);
}

{int_lit}       { fprintf(token_out, "INTEGER_LITERAL %s\n", yytext); }
{str_lit}       { fprintf(token_out, "STRING_LITERAL %s\n", yytext); }

"="             { fprintf(token_out, "ASSIGN\n"); }
"=="            { fprintf(token_out, "EQ\n"); }
"<"             { fprintf(token_out, "LT\n"); }
"<="            { fprintf(token_out, "LE\n"); }
">"             { fprintf(token_out, "GT\n"); }
">="            { fprintf(token_out, "GE\n"); }
"+"             { fprintf(token_out, "PLUS\n"); }
"-"             { fprintf(token_out, "MINUS\n"); }
"*"             { fprintf(token_out, "MUL\n"); }
"/"             { fprintf(token_out, "DIV\n"); }

"("             { fprintf(token_out, "LPAREN\n"); }
")"             { fprintf(token_out, "RPAREN\n"); }
"["             { fprintf(token_out, "LBRACK\n"); }
"]"             { fprintf(token_out, "RBRACK\n"); }
"{"             { fprintf(token_out, "LBRACE\n"); }
"}"             { fprintf(token_out, "RBRACE\n"); }
","             { fprintf(token_out, "COMMA\n"); }
";"             { fprintf(token_out, "SEMICOLON\n"); }

[ \t\r\n]+      ;      // ignore whitespace
"//".*          ;      // ignore comments

.               { fprintf(stderr, "Invalid character: %s\n", yytext); }

%%

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: %s <source_file>\n", argv[0]);
        return 1;
    }
    FILE* source = fopen(argv[1], "r");
    token_out = fopen("token_stream.txt", "w");
    if (!source || !token_out) {
        perror("File error");
        return 1;
    }
    yyin = source;
    yylex();
    fclose(source);
    fclose(token_out);
    return 0;
}

int yywrap() {
    return 1;
}
