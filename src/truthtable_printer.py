#encoding:utf8
'''
Created on 04.05.2010

@author: ranux
'''

import re

def parse(logical_expression):
  """
  >>> parse("p")
  {'p': ['1', '0']}
  >>> parse("NOT p")
  {'p': ['1', '0']}
  >>> parse("p OR q AND 293")
  {'q': ['0', '1', '0', '1'], 'p': ['0', '0', '1', '1']}
  """
  result = {}
  
  tokens = re.findall('[a-z]+', logical_expression)

  for t in tokens:
    result[t] = []
    
  if len(tokens) == 1:
    result[logical_expression] = [v for v in bin(2)[2:]]
    return result  
  
  max_combinations = 2 ** len(tokens)
  for num in range(0, max_combinations):
    bin_num = bin(num)[2:]  # remove 0b
    
    while len(bin_num) < len(tokens):
      bin_num = '0' + bin_num
    for c, t in zip(bin_num, tokens):
      result[t].append(c)
   
  return result


class LogicalValue():
  def __init__(self, name, values=[], reverse=False):
    self.name  = name
    self.values = values 
    self.reverse = reverse  # for print in reverse order
  
  def OR(self, other):
    """ Logical value OR other logical value. Returns result of union ( LogicalValue  )
    >>> val1 = LogicalValue('p', [1,1,0,0])
    >>> val2 = LogicalValue('q', [1,0,1,0])
    >>> val1.OR(val2)
    p OR q [1, 1, 1, 0]
    >>> val1 = LogicalValue('p', [1,1,1,1,0,0,0,0])
    >>> val2 = LogicalValue('q', [1,1,0,0,1,1,0,0])
    >>> val1.OR(val2)
    p OR q [1, 1, 1, 1, 1, 1, 0, 0]
    """
    new_values = []
    for v, ov in zip(self.values, other.values):
      new_values.append(int(v) or int(ov))

    return LogicalValue(self.name+' OR '+other.name, new_values)
  
  def AND(self, other):
    """ Logical value AND other logical value. Returns result of intersection ( LogicalValue )
    >>> val1 = LogicalValue('p', [1,1,0,0])
    >>> val2 = LogicalValue('q', [1,0,1,0])
    >>> val1.AND(val2)
    p AND q [1, 0, 0, 0]
    """
    new_values = []
    for v, ov in zip(self.values, other.values):
      new_values.append(int(v) and int(ov))

    return LogicalValue(self.name+' AND '+other.name, new_values)

  def NOT(self):
    """ Apply unary operator for self. Returns flipped copy of LogicalValue
    >>> val1 = LogicalValue('p', [1,1,0,0])
    >>> val1.NOT()
    NOT p [0, 0, 1, 1]
    """
    return LogicalValue('NOT '+self.name, [int(not int(v)) for v in self.values])
    
  def __repr__(self):
    result = self.name + ' '
    if self.reverse:
      copy = self.values[:]
      copy.reverse()
      result += copy.__repr__()
    else:
      result += self.values.__repr__()
    return result
  

tokens = ('VALUE','OR','AND','NOT','LPAREN','RPAREN',)

t_OR    = r'OR'
t_AND  = r'AND'
t_NOT  = r'NOT'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_VALUE(t):
    r'[a-z][a-z0-9_]*'
    t.value = LogicalValue(t.value, init_logical_vals[t.value])
    return t
  
t_ignore = " \t"
  
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lex.lex()

import doctest
doctest.testmod()
    
#for tok in lexer:
#    print tok
#
## Parsing rules
precedence = ( ('left','OR'), 
                      ('left','AND'), 
                      ('right','NOT'),)

def p_statement_expr(p):
    'statement : expression'
    #p[1].reverse = True
    print(p[1])
      
def p_expression_or(p):
  """expression : expression OR expression
  """
  p[0] = p[1].OR(p[3])

def p_expression_and(p):
  """expression : expression AND expression
  """
  p[0] = p[1].AND(p[3])

def p_expression_not(p):
  """expression : NOT expression
  """
  p[0] = p[2].NOT()
  
def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]
       
def p_expression_value(p):
    "expression : VALUE"
    p[0] = p[1]

    
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")
    
import ply.yacc as yacc    
yacc.yacc()
  
while 1:
  try:
    s = raw_input('> ')
    init_logical_vals = parse(s)
  except EOFError:
    break
  if not s: continue
  yacc.parse(s)