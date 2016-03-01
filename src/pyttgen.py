#encoding:utf8
'''
Created on 04.05.2010
Copyright (C) 2010 Alexander S. Razzhivin ( site https://github.com/RANUX/ )

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re
import doctest
import ply.lex as lex
import ply.yacc as yacc  


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
  if 'quit' in tokens or 'exit' in tokens:
    exit(0)
    
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
  
  def IMPL(self, other):
    """implication"""
    new_values = []
    for v, ov in zip(self.values, other.values):
      if int(v) == 1 and int(ov) == 0:
        new_values.append(0)
      else:
        new_values.append(1)
  
    return LogicalValue(self.name+' -> '+other.name, new_values)
  
  def EQUALS(self, other):
    return self.IMPL(other).AND(other.IMPL(self))  
  
  def __eq__(self, other):
    return self.name == other.name and self.values == other.values
  
  def __repr__(self):
    return self.values.__repr__() + ' ' + self.name
  

class TruthTableConstructor:
  
  def __init__(self):
    lex.lex(module=self)
    yacc.yacc(module=self)
    self.table = []

    
  def build(self, proposition):
    self.init_logical_vals = parse(proposition)
    yacc.parse(proposition)
    
  def run(self):  
    while 1:
      self.table = []
      try:
        s = raw_input('> ')
        self.init_logical_vals = parse(s)
        for k,lst in self.init_logical_vals.items():
          print [int(v) for v in lst], ' ', k
      except EOFError:
        break
      if not s: continue
      yacc.parse(s)
      for logval in self.table:
        print logval

  tokens = ('VALUE', 'EQUALS','IMPL','OR','AND','NOT','LPAREN','RPAREN',)
  
  t_EQUALS = r'EQUALS|\<\-\>'
  t_IMPL = r'IMPL|\-\>'
  t_OR   = r'OR|\+|\|'
  t_AND  = r'AND|\*|\&'
  t_NOT  = r'NOT|~'
  t_LPAREN  = r'\('
  t_RPAREN  = r'\)'
  
  def t_VALUE(self, t):
      r'[a-z][a-z0-9_]*'
      t.value = LogicalValue(t.value, self.init_logical_vals[t.value])
      return t
    
  t_ignore = " \t"
    
  def t_newline(self, t):
      r'\n+'
      t.lexer.lineno += t.value.count("\n")
      
  def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)
  
  precedence = ( ('left', 'EQUALS'),
                 ('left', 'IMPL'),
                 ('left','OR'), 
                 ('left','AND'), 
                 ('right','NOT'),)
  
  def p_expression_equals(self, p):
    """expression : expression EQUALS expression
    """ 
    p[0] = p[1].EQUALS(p[3])
    p[0].name = p[1].name +' <-> '+p[3].name
    self.table.append(p[0])
    
  def p_expression_impl(self, p):
    """expression : expression IMPL expression
    """ 
    p[0] = p[1].IMPL(p[3])
    self.table.append(p[0])
        
  def p_expression_or(self, p):
    """expression : expression OR expression
    """
    p[0] = p[1].OR(p[3])
    self.table.append(p[0])

  
  
  def p_expression_and(self, p):
    """expression : expression AND expression
    """
    p[0] = p[1].AND(p[3])
    self.table.append(p[0])

  
  
  def p_expression_not(self, p):
    """expression : NOT expression
    """
    p[0] = p[2].NOT()
    self.table.append(p[0])

    
  def p_expression_group(self, p):
          'expression : LPAREN expression RPAREN'
          p[2].name = '('+p[2].name+')'
          p[0] = p[2]
         
  def p_expression_value(self, p):
      "expression : VALUE"
      p[0] = p[1]
  
  
      
  def p_error(self, p):
      if p:
          print("Syntax error at '%s'" % p.value)
      else:
          print("Syntax error at EOF")
      


if __name__ == '__main__':
    doctest.testmod()
    ttconstructor = TruthTableConstructor()
    ttconstructor.run()
