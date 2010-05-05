#encoding:utf8
'''
Created on 04.05.2010

@author: ranux
'''

import re


def remove_duplicates(values):
  """
  Given a list of numbers, return a list where
  all adjacent == elements have been reduced to a single element,
  so [1, 2, 2, 3] returns [1, 2, 3].
  """
  result = []
  for val in values:
    if not result.count(val):
      result.append(val)
  return result

def parse(logical_expression):
  """
  >>> parse("p")
  {'p': ['1', '0']}
  >>> parse("NOT p")
  {'p': ['1', '0']}
  >>> parse("p OR q AND 293")
  {'q': ['0', '1', '0', '1'], 'p': ['0', '0', '1', '1']}
  >>> parse("p AND p")
  {'p': ['1', '0']}
  """
  result = {}
  
  tokens = re.findall('[a-z]+', logical_expression)

  tokens = sorted(remove_duplicates(tokens))
  for t in tokens:
    result[t] = []

  if len(tokens) == 1:
    result[tokens[0]] = [v for v in bin(2)[2:]]
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
  def __init__(self, name, values=[]):
    self.name  = name
    self.values = values 

  def OR(self, other):
    """ Logical value OR other logical value. Returns result of union ( LogicalValue  )
    >>> val1 = LogicalValue('p', [1,1,0,0])
    >>> val2 = LogicalValue('q', [1,0,1,0])
    >>> val1.OR(val2)
    [1, 1, 1, 0] p OR q
    >>> val1 = LogicalValue('p', [1,1,1,1,0,0,0,0])
    >>> val2 = LogicalValue('q', [1,1,0,0,1,1,0,0])
    >>> val1.OR(val2)
    [1, 1, 1, 1, 1, 1, 0, 0] p OR q
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
    [1, 0, 0, 0] p AND q
    """
    new_values = []
    for v, ov in zip(self.values, other.values):
      new_values.append(int(v) and int(ov))

    return LogicalValue(self.name+' AND '+other.name, new_values)

  def NOT(self):
    """ Apply unary operator for self. Returns flipped copy of LogicalValue
    >>> val1 = LogicalValue('p', [1,1,0,0])
    >>> val1.NOT()
    [0, 0, 1, 1] NOT p
    """
    return LogicalValue('NOT '+self.name, [int(not int(v)) for v in self.values])
    
  def __repr__(self):
    return self.values.__repr__() + ' ' + self.name
  

tokens = ('VALUE','OR','AND','NOT','LPAREN','RPAREN',)

t_OR    = r'OR|\+|\|'
t_AND  = r'AND|\*|\&'
t_NOT  = r'NOT|~'
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
    #print(p[1])
    pass
      
def p_expression_or(p):
  """expression : expression OR expression
  """
  p[0] = p[1].OR(p[3])
  print p[0]


def p_expression_and(p):
  """expression : expression AND expression
  """
  p[0] = p[1].AND(p[3])
  print p[0]


def p_expression_not(p):
  """expression : NOT expression
  """
  p[0] = p[2].NOT()
  print p[0]
  
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
    for k,lst in init_logical_vals.items():
      print [int(v) for v in lst], ' ', k
  except EOFError:
    break
  if not s: continue
  yacc.parse(s)