#! /usr/bin/env python

from string import *
import sys
from ast import *
from tokens import *
from parser import *
from grfstrings import *
from generic import ScriptError

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

def p_error(p):
    if p == None: print "Unexpected EOF"
    else:
        print p
        print "Syntax error at '%s', line %d" % (p.value, p.lineno)
    sys.exit(2)

import ply.yacc as yacc
parser = yacc.yacc(debug=True)
script = open('data.nml', 'r').read().strip()
if script == "": print "Empty input file"
result = parser.parse(script)
print_script(result, 0)

read_lang_files()

outf = open('data.nfo', 'w')

actions = []
for block in result:
    actions.extend(block.get_action_list())

outf.write(
'''// Automatically generated by GRFCODEC. Do not modify!
// (Info version 7)
// Escapes: 2+ = 71 = D= = DR 2- = 70 = D+ = DF 2< = 7= = D- = DC 2> = 7! = Du* = DM 2u< = 7< = D* = DnF 2u> = 7> = Du<< = DnC 2/ = 7G = D<< = DO 2% = 7g = D& 2u/ = 7gG = D| 2u% = 7GG = Du/ 2* = 7gg = D/ 2& = 7c = Du% 2| = 7C = D% 2^ 2sto = 2s 2rst = 2r 2+ 2ror = 2rot
// Format: spritenum pcxfile xpos ypos compression ysize xsize xrel yrel
-1 * 4 00 00 00 00

''')


for action in actions:
    action.write(outf)

outf.close()
