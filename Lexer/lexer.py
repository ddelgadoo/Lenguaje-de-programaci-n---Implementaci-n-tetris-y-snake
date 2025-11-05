from __future__ import unicode_literals
import Lexer.Tokens as Tokens
import re

"""CLASSES"""


class RegexPattern(object): # Hereda de (object)
    def __init__(self, regex, handler):
        self.regex = regex
        self.handler = handler


""" The Lexer object consists on 5 attributes.
pos = Current index of the source string
line = Current line on source 
source = The source code
tokens = An array of token type objects
patterns = An array of regex type handlers patterns."""


class Lexer(object): # Hereda de (object)
    def __init__(self, source):
        self.pos = 0
        self.line = 1
        self.source = source
        self.Tokens = []
        self.patterns = [
            RegexPattern(re.compile(u"\s+"), skipHandler),                               # ur"\s+" Matches one or more white spaces characters, i.e, \n,\tab, " ", etc.
                                                                                         # ur" is the sintax for raw unicode string

            RegexPattern(re.compile(u"//.*"), commentHandler),                               # ur"//.*" For comment lines like // Hello or //////// hello

            RegexPattern(re.compile(u'"[^"]*"'), stringHandler),                             # Matches a string enclosed within double quotes: "JIJI jajaja"

            RegexPattern(re.compile(u"[0-9]+(\.[0-9]+)?"), numberHandler),                   # [0-9]+ Matches a single or more digit numbers from zero to nine.
                                                                                             # (\.[0-9]+)?") Is a group that matches the decimal part of the number.

            RegexPattern(re.compile(u"[a-zA-Z_][a-zA-Z0-9_]*"), symbolHandler),              # [a-zA-Z_] Matches the first character of the identifier

            RegexPattern(re.compile(u"\["), defaultHandler(Tokens.TokenKind.OPEN_BRAC, u"[")),
            RegexPattern(re.compile(u"\]"), defaultHandler(Tokens.TokenKind.CLOSED_BRAC, u"]")),
            RegexPattern(re.compile(u"\{"), defaultHandler(Tokens.TokenKind.OPEN_CURL, u"{")),
            RegexPattern(re.compile(u"\}"), defaultHandler(Tokens.TokenKind.CLOSED_CURL, u"}")),
            RegexPattern(re.compile(u"\("), defaultHandler(Tokens.TokenKind.OPEN_PARENT, u"(")),
            RegexPattern(re.compile(u"\)"), defaultHandler(Tokens.TokenKind.CLOSED_PARENT, u")")),
            RegexPattern(re.compile(u"=="), defaultHandler(Tokens.TokenKind.EQUAL, u"==")),
            RegexPattern(re.compile(u"!="), defaultHandler(Tokens.TokenKind.NOT_EQUAL, u"!=")),
            RegexPattern(re.compile(u"="), defaultHandler(Tokens.TokenKind.ASSIGNMENT, u"=")),
            RegexPattern(re.compile(u"!"), defaultHandler(Tokens.TokenKind.NOT, u"!")),
            RegexPattern(re.compile(u"<="), defaultHandler(Tokens.TokenKind.LESS_EQUAL, u"<=")),
            RegexPattern(re.compile(u"<"), defaultHandler(Tokens.TokenKind.LESS, u"<")),
            RegexPattern(re.compile(u">="), defaultHandler(Tokens.TokenKind.GREATER_EQUAL, u">=")),
            RegexPattern(re.compile(u">"), defaultHandler(Tokens.TokenKind.GREATER, u">")),
            RegexPattern(re.compile(u"\|\|"), defaultHandler(Tokens.TokenKind.OR, u"||")),
            RegexPattern(re.compile(u"&&"), defaultHandler(Tokens.TokenKind.AND, u"&&")),
            RegexPattern(re.compile(u"\."), defaultHandler(Tokens.TokenKind.DOT, u".")),
            RegexPattern(re.compile(u";"), defaultHandler(Tokens.TokenKind.SEMICOMMA, u";")),
            RegexPattern(re.compile(u":"), defaultHandler(Tokens.TokenKind.COLON, u":")),
            RegexPattern(re.compile(u"\?"), defaultHandler(Tokens.TokenKind.QUESTION, u"?")),
            RegexPattern(re.compile(u","), defaultHandler(Tokens.TokenKind.COMMA, u",")),
            RegexPattern(re.compile(u"\+\+"), defaultHandler(Tokens.TokenKind.PLUS_PLUS, u"++")),
            RegexPattern(re.compile(u"--"), defaultHandler(Tokens.TokenKind.MINUS_MINUS, u"--")),
            RegexPattern(re.compile(u"\+="), defaultHandler(Tokens.TokenKind.PLUS_EQUAL, u"+=")),
            RegexPattern(re.compile(u"-="), defaultHandler(Tokens.TokenKind.MINUS_EQUAL, u"-=")),
            RegexPattern(re.compile(u"\+"), defaultHandler(Tokens.TokenKind.PLUS, u"+")),
            RegexPattern(re.compile(u"-"), defaultHandler(Tokens.TokenKind.DASH, u"-")),
            RegexPattern(re.compile(u"/"), defaultHandler(Tokens.TokenKind.SLASH, u"/")),
            RegexPattern(re.compile(u"\*"), defaultHandler(Tokens.TokenKind.STAR, u"*")),
            RegexPattern(re.compile(u"%"), defaultHandler(Tokens.TokenKind.PERCENT, u"%")),
        ]

    def advanceN(self, n):
        self.pos += n

    def at(self):
        return self.source[self.pos]

    def advance(self):
        self.pos += 1

    def remainder(self):
        return self.source[self.pos:]

    def push(self, token):
        self.Tokens.append(token)

    def at_eof(self):
        return self.pos >= len(self.source)


"""----------------------------------------------------------------------------"""

"""GLOBAL FUNCTIONS"""
"""Tokenizer: """


def tokenize(source):
    lex = Lexer(source)
    while not lex.at_eof():
        matched = False  # Assume that no pattern has matched
        for pattern in lex.patterns:
            loc = pattern.regex.match(lex.remainder())  # Looks for a coincidence between the pattern that we are on, and the remaining string source code
            if loc is not None and loc.start() == 0:    # If we find a match object (loc not none) and the index of the coincidence is zero (Because we only want to accept tokens
                                                        # at the beginning of the remaining string source code) then:

                pattern.handler(lex, pattern.regex)     # We call the handler associated to that pattern. The handler is in charge of creating the token, and moving along the
                                                        # source code.
                matched = True                          # Indicates that there was a match.
                break                                   # We break the for cycle because there is a pattern that matched on the position 0 of the remainder of the code.

        if not matched:                                 # The code went along the patterns array and did not find any match
            # Reemplazo de f-string con .format()
            raise Exception(u"lexer error: unrecognized token near {0}".format(lex.remainder()))

    lex.push(Tokens.newToken(Tokens.TokenKind.IOF, u"EOF")) #Means that we are at the End Of the File
    return lex.Tokens


"""----------------------------------------------------------------------------"""
"""Handlers"""


def defaultHandler(kind, value):
    def handler(lex, _regex):                   # Note that the default handlers are already initialized on the lexer, so if we find any character on the
                                                # source code that is managed by default, it will return the inside function handler(lex, pattern.regex).

        lex.advanceN(len(value))                #Depending on the pattern that we find, the lexer moves to pos = pos + len(value),
        lex.push(Tokens.newToken(kind, value))  # We create a new token for the pattern and append it to the tokens array.

    return handler


def stringHandler(lex, regex):
    match = regex.match(lex.remainder())                                  # Assigns the object match on the remainder position to match
    stringLiteral = lex.remainder()[match.start():match.end()]            # lex.remainder() is a string, because python treats the strings as arrays, we can make list slicing
                                                                          # recall that the method .start() of object match returns the index  of the string in which the match
                                                                          # of the regex began, on the tokenizer this should always be 0. .end() returns the index in which finishes
                                                                          # the match. So stringLiteral is the string from position match.start() to match.end()

    lex.push(Tokens.newToken(Tokens.TokenKind.STRING, stringLiteral))     # We create the new token
    lex.advanceN(len(stringLiteral))                                      # Advance the len of the string


def numberHandler(lex, regex):                                            #Similar to stringHandler
    match = regex.match(lex.remainder())
    num = match.group(0)                                                  # Because the regex of the numeric patterns are groups [0-9]+ and (\.[0-9])? we want the whole match (group(0))
    lex.push(Tokens.newToken(Tokens.TokenKind.NUMBER, num))
    lex.advanceN(len(num))


def symbolHandler(lex, regex):
    match = regex.match(lex.remainder())
    if not match:                                                         # If match is empty (Because python treats empty as falsy), we go out from the symHandler so the tokenizer
                                                                          # looks for other patterns
        return

    sym = match.group(0)

    kind = Tokens.reserved_lu.get(sym.lower(), Tokens.TokenKind.IDENTIFIER) # Reserved-Lu is a dictionary on class Tokens which has the reserved words, .get() looks sym() in lower case
                                                                            # (so the lexer allows now capital and lower case for the reserved words.) and returns its value. If we don't
                                                                            # find any coincidence on the dictionary it means that the word is defined as a variable, so it will have a
                                                                            # tokenKind = Identifier.

    lex.push(Tokens.newToken(kind, sym))
    lex.advanceN(len(sym))


def skipHandler(lex, regex):
    match = regex.match(lex.remainder())
    lex.advanceN(match.end())


def commentHandler(lex, regex):
    match = regex.match(lex.remainder())
    if match is not None:
        lex.advanceN(match.end())
        lex.line += 1
