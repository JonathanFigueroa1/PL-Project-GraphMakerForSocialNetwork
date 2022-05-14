import ply.lex as lex 
import ply.yacc as yacc
import sys

# In here we create the tokens for the project 

tokens = [

    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MULTIPLY',
    'EQUALS',
    'DIVIDE',
    'MINUS',
    
]

#Tokens representations

t_PLUS = r'\+'
t_DIVIDE = r'\/'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='
t_ignore = r' '

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print("Characters not recognized,enter another")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (

    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

def p_calculator(p):
    '''
    calculator : expression
               | var_assign
               | empty
    
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression 
    '''
    p[0] = ('=', p[1], p[3])

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression MINUS expression 
               | expression PLUS expression 
               | expression DIVIDE expression 
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    
    
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME

    '''
    p[0] = ('var', p[1])

def p_error(p):
    print("Syntax Error")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


parser = yacc.yacc()


env = {}
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
        elif p[0] == 'var':
            if p[1] not in env:
                return 'variable not found'
            else:
                return env[p[1]]

    else:
        return p

while True:
    try:
        s = input('SIM >> ')
    except EOFError:
        break
    parser.parse(s)

