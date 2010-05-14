#encoding:utf8
'''
Created on 12.05.2010
Copyright (C) 2010 Alexander S. Razzhivin ( site http://httpbots.com )

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
import unittest
from pyttgen import TruthTableConstructor
from pyttgen import LogicalValue

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