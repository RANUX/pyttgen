'''
Created on 12.05.2010

@author: Alexander S. Razzhivin
'''
import unittest
from truthtable_constructor import *

class Test(unittest.TestCase):


    def testAND(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("p AND q")
      assert ttconstructor.table[0] == LogicalValue("p AND q", [0, 0, 0, 1])
      
    def testOR(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("p OR q")
      assert ttconstructor.table[0] == LogicalValue("p OR q", [0, 1, 1, 1])
      
    def testNOT(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("NOT p")
      assert ttconstructor.table[0] == LogicalValue("NOT p", [0, 1])
    
    def test_group(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("p AND (q OR r)")
      assert ttconstructor.table[1] == LogicalValue("p AND (q OR r)", [0, 0, 0, 0, 0, 1, 1, 1])
      
    def test_implication(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("p -> q")
      assert ttconstructor.table[0] == LogicalValue("p -> q", [1, 1, 0, 1])
      
    def test_equality(self):
      ttconstructor = TruthTableConstructor()
      ttconstructor.build("p <-> q")
      assert ttconstructor.table[0] == LogicalValue("p <-> q", [1, 0, 0, 1])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()