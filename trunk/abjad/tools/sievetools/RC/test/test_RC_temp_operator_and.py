from abjad.tools.sievetools.RC import RC
from abjad.tools.sievetools.RCExpression import RCExpression
import py.test


def test_rc_operator_and_01( ):
   '''RC AND RC returns a RCExpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   t = rc1 & rc2

   assert isinstance(t, RCExpression)
   assert t.operator == 'and'
   assert t.rcs == [rc1, rc2]
   assert t.get_boolean_train(4) == [0,0,0,0]
   assert t.get_congruent_bases(6) == [ ]


def test_rc_operator_and_02( ):
   '''and-RCExpression AND RC returns a flat and-RCExpression.'''

   rcexpression = RC(4, 0) & RC(4, 1)
   rc = RC(3, 0)
   t = rc & rcexpression

   assert isinstance(t, RCExpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_and_03( ):
   '''RC AND and-RCExpression returns a flat and-RCExpression.'''

   rcexpression = RC(4, 0) & RC(4, 1)
   rc = RC(3, 0)
   t = rcexpression & rc

   assert isinstance(t, RCExpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_and_04( ):
   '''and-RCExpression AND and-RCExpression returns a flat and-RCExpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   rcsA = rc1 & rc2
   rcsB = rc3 & rc4
   t = rcsA & rcsB

   assert isinstance(t, RCExpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 4
   assert rc1 in t.rcs
   assert rc2 in t.rcs
   assert rc3 in t.rcs
   assert rc4 in t.rcs


def test_rc_operator_and_05( ):
   '''AND'''

   t = RC(2, 0) & RC(3, 0)

   assert isinstance(t, RCExpression)
   assert t.operator == 'and'
   assert t.get_boolean_train(6) == [1,0,0,0,0,0]
   assert t.get_congruent_bases(6) == [0, 6]


def test_rc_operator_and_06( ):
   '''AND'''

   t = RC(2, 1) & RC(3, 0)

   assert t.get_boolean_train(6) == [0,0,0,1,0,0]
   assert t.get_congruent_bases(6) == [3]
