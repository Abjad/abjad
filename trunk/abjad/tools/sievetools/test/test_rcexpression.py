from abjad.tools.sievetools.RCExpression import RCExpression
from abjad.tools.sievetools.RC import RC
import py.test

## OR ##

def test_rcexpression_01( ):
   '''boolean operator defaults to OR.'''

   t = RCExpression([RC(2, 0), RC(3, 0)])

   assert t.operator == 'or'


def test_rcexpression_02( ):

   t = RCExpression([RC(2, 0), RC(3, 0)])

   assert t.get_boolean_train(6) == [1,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_rcexpression_03( ):

   t = RCExpression([RC(2, 1), RC(3, 0)])

   assert t.get_boolean_train(6) == [1,1,0,1,0,1]
   assert t.get_congruent_bases(6) == [0,1,3,5,6]


## AND ##

def test_rcexpression_04( ):

   t = RCExpression([RC(2, 0), RC(3, 0)], 'and')

   assert t.operator == 'and'
   assert t.get_boolean_train(6) == [1,0,0,0,0,0]
   assert t.get_congruent_bases(6) == [0, 6]


def test_rcexpression_05( ):

   t = RCExpression([RC(2, 1), RC(3, 0)], 'and')

   assert t.get_boolean_train(6) == [0,0,0,1,0,0]
   assert t.get_congruent_bases(6) == [3]


## XOR ##

def test_rcexpression_06( ):

   t = RCExpression([RC(2, 0), RC(3, 0)], 'xor')

   assert t.operator == 'xor'
   assert t.get_boolean_train(6) == [0,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [2,3,4]


def test_rcexpression_07( ):

   t = RCExpression([RC(2, 1), RC(3, 0)], 'xor')

   assert t.get_boolean_train(6) == [1,1,0,0,0,1]
   assert t.get_congruent_bases(6) == [0,1,5,6]


