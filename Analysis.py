
# Jonathan Figueroa Perez 
# ICOM4036 Proyecto FINAL 
# A programming Language for Social Network Analysis. 
 

import networkx as nx
import ply.lex as lex
import ply.yacc as yacc
import TABLES as T

#lexer part

reserved = {
    'if' : 'IF',
    'in' : 'IN',
    'else': 'ELSE',
    'for' : 'FOR',
    'from' : 'FROM',
    'while' : 'WHILE',
    'display' : 'DISPLAY',
    'node'  :   'NODE',
    '-' :   'MINUS',
    '+' :   'PLUS',
    '//' : 'LEFTSLASHES',
    '\\\\' : 'RIGHTSLASHES',
    'Analysis' : 'Analysis',
    'operations'    :   'OPERATIONS',
    'create' : 'CREATE'
}
tokens = [
    'CHARACTER',
    'ID',
    'LEFTDELIMITER',
    'RIGHTDELIMITER',
    'COMMA',
    'SEPARATOR',
    'DOT',
    'BINOP',

] + (list(reserved.values()))
t_ignore = ' '
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  
    return t


t_LEFTSLASHES = r'//'
t_RIGHTSLASHES = r'\\\\'
t_COMMA = r'\,'
t_BINOP = r'[>=|<|<=|>|!=|==]'
t_DOT = r'\.'
t_MINUS = r'-'
t_PLUS = r'\+'
t_SEPARATOR = r'\;'
t_LEFTDELIMITER = r'\['
t_RIGHTDELIMITER = r'\]'


def t_error(t):
    print("Illegal character '%s" %t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()


# Parser

def Information():
    print(''' This program is for people that want an easy way to create data tables for social network Analysis. 
    ''')

def p_define(p):
    'define : Analysis function'
    p[0]= p[2]


def p_function(p):
    '''function : term
               | FOR LEFTSLASHES term IN term RIGHTSLASHES function
               | WHILE LEFTSLASHES term BINOP term RIGHTSLASHES term'''

    if('for' in p):
        print('for loop')
    if('while' in p):
        print("while loop")
    p[0] = p[1]



def p_add(p) :
    '''add : graph PLUS LEFTDELIMITER file RIGHTDELIMITER
            | graph PLUS ID'''

    if(len(p)>4):
        p[0] = T.add(p[4], p[1])
    else: T.addNode(p[1], p[3])




def p_create(p):
    '''create : CREATE LEFTSLASHES ID RIGHTSLASHES
                | CREATE LEFTSLASHES ID FROM file RIGHTSLASHES
                | CREATE'''

    if(len(p)>6):
        p[0] = T.createGraphFromFile(p[3], p[5])
    elif(len(p)>3):
        p[0]= T.createGraph(p[3])
    else:
        p[0]= T.createNewGraph()
def p_remove(p) :
    'remove : graph MINUS node'
    p[0] = T.remove(p[3], p[1])

def p_display(p):
    'display : DISPLAY graph'
    p[0]=T.displayGraph(p[2])

def p_operations(p):
    'operations : graph OPERATIONS'
    p[0] = T.operations(p[1])

def p_graph(p):
    'graph : ID'
    p[0] = p[1]

def p_file(p) :
    'file : ID DOT ID'
    p[0] = p[1]+p[2]+p[3]
def p_node(p) :
    'node : NODE ID'
    p[0] = T.getNode(p[2])

def p_term(p) :
    '''term : add
            | remove
            | display
            | file
            | graph
            | node
            | create
            | operations'''
    p[0] = p[1]

def p_error(p):
    print('Syntax error!', s)

parser = yacc.yacc()
while True:
   try:
       s = input('ANALYSIS> ')
   except EOFError:
       break
   if(s=="exit"):
       input('You are about to exit you are sure? Press enter.')
       break
   if(s=='About'):
       Information()
       continue
   if not s: continue
   result = parser.parse(s)