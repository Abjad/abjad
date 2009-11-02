from abjad.tools.sievetools.rc import RC
from abjad.tools.sievetools.rcexpression import RCexpression
import py.test

## AND ##

def test_rc_operator_and_01( ):
   '''RC AND RC returns a RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   t = rc1 & rc2

   assert isinstance(t, RCexpression)
   assert t.operator == 'and'
   assert t.rcs == [rc1, rc2]
   assert t.get_boolean_train(4) == [0,0,0,0]
   assert t.get_congruent_bases(6) == [ ]


def test_rc_operator_and_02( ):
   '''and-RCexpression AND RC returns a flat and-RCexpression.'''

   rcexpression = RC(4, 0) & RC(4, 1)
   rc = RC(3, 0)
   t = rc & rcexpression

   assert isinstance(t, RCexpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_and_03( ):
   '''RC AND and-RCexpression returns a flat and-RCexpression.'''

   rcexpression = RC(4, 0) & RC(4, 1)
   rc = RC(3, 0)
   t = rcexpression & rc

   assert isinstance(t, RCexpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_and_04( ):
   '''and-RCexpression AND and-RCexpression returns a flat and-RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   rcsA = rc1 & rc2
   rcsB = rc3 & rc4
   t = rcsA & rcsB

   assert isinstance(t, RCexpression)
   assert t.operator == 'and'
   assert len(t.rcs) == 4
   assert rc1 in t.rcs
   assert rc2 in t.rcs
   assert rc3 in t.rcs
   assert rc4 in t.rcs


def test_rc_operator_and_05( ):
   '''AND'''

   t = RC(2, 0) & RC(3, 0)

   assert isinstance(t, RCexpression)
   assert t.operator == 'and'
   assert t.get_boolean_train(6) == [1,0,0,0,0,0]
   assert t.get_congruent_bases(6) == [0, 6]


def test_rc_operator_and_06( ):
   '''AND'''

   t = RC(2, 1) & RC(3, 0)

   assert t.get_boolean_train(6) == [0,0,0,1,0,0]
   assert t.get_congruent_bases(6) == [3]


## OR ##

def test_rc_operator_or_01( ):
   '''RC OR RC returns a RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   t = rc1 | rc2

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert t.rcs == [rc1, rc2]


def test_rc_operator_or_02( ):
   '''or-RCexpression OR RC returns a flat or-RCexpression.'''

   rcexpression = RC(4, 0) | RC(4, 1)
   rc = RC(3, 0)
   t = rc | rcexpression

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_or_03( ):
   '''RC OR or-RCexpression returns a flat or-RCexpression.'''

   rcexpression = RC(4, 0) | RC(4, 1)
   rc = RC(3, 0)
   t = rcexpression | rc

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_or_04( ):
   '''or-RCexpression OR or-RCexpression returns a flat or-RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   rcsA = rc1 | rc2
   rcsB = rc3 | rc4
   t = rcsA | rcsB

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert len(t.rcs) == 4
   assert rc1 in t.rcs
   assert rc2 in t.rcs
   assert rc3 in t.rcs
   assert rc4 in t.rcs


def test_rc_operator_or_05( ):
   '''OR''' 

   t = RC(2, 0) | RC(3, 0)

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert t.get_boolean_train(6) == [1,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_rc_operator_or_06( ):
   '''OR''' 

   t = RC(2, 1) | RC(3, 0)

   assert t.get_boolean_train(6) == [1,1,0,1,0,1]
   assert t.get_congruent_bases(6) == [0,1,3,5,6]



## XOR ##

def test_rc_operator_xor_01( ):
   '''RC XOR RC returns a RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   t = rc1 ^ rc2

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert t.rcs == [rc1, rc2]


def test_rc_operator_xor_02( ):
   '''xor-RCexpression XOR RC returns a flat xor-RCexpression.'''

   rcexpression = RC(4, 0) ^ RC(4, 1)
   rc = RC(3, 0)
   t = rc ^ rcexpression

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_xor_03( ):
   '''RC XOR xor-RCexpression returns a flat xor-RCexpression.'''

   rcexpression = RC(4, 0) ^ RC(4, 1)
   rc = RC(3, 0)
   t = rcexpression ^ rc

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert len(t.rcs) == 3
   assert rcexpression.rcs[0] in t.rcs
   assert rcexpression.rcs[1] in t.rcs
   assert rc in t.rcs


def test_rc_operator_xor_04( ):
   '''xor-RCexpression XOR xor-RCexpression returns a flat xor-RCexpression.'''

   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   rcsA = rc1 ^ rc2
   rcsB = rc3 ^ rc4
   t = rcsA ^ rcsB

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert len(t.rcs) == 4
   assert rc1 in t.rcs
   assert rc2 in t.rcs
   assert rc3 in t.rcs
   assert rc4 in t.rcs


def test_rc_operator_xor_05( ):
   '''XOR'''

   t = RC(2, 0) ^ RC(3, 0)

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert t.get_boolean_train(6) == [0,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [2,3,4]


def test_rc_operator_xor_06( ):
   '''XOR'''

   t = RC(2, 1) ^ RC(3, 0)

   assert t.get_boolean_train(6) == [1,1,0,0,0,1]
   assert t.get_congruent_bases(6) == [0,1,5,6]


## MIXED ##

def test_rc_operator_mixed_01( ):
   '''Mixed operators yield nested RCexpressions.'''
   
   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   
   rcsA = rc1 & rc2
   rcsB = rc3 | rc4
   t = rcsA ^ rcsB

   assert isinstance(t, RCexpression)
   assert t.operator == 'xor'
   assert len(t.rcs) == 2
   assert isinstance(t.rcs[0], RCexpression)
   assert t.rcs[0].operator == 'and'
   assert isinstance(t.rcs[1], RCexpression)
   assert t.rcs[1].operator == 'or'
   assert t.rcs[0] is rcsA
   assert t.rcs[1] is rcsB


def test_rc_operator_mixed_02( ):
   '''Mixed operators yield nested RCexpressions. 
   RCexpressions with the same operator, merge.'''
   
   rc1 = RC(4, 0) 
   rc2 = RC(4, 1)
   rc3 = RC(3, 0) 
   rc4 = RC(3, 1)
   
   rcsA = rc1 & rc2
   rcsB = rc3 | rc4
   t = rcsA | rcsB

   assert isinstance(t, RCexpression)
   assert t.operator == 'or'
   assert len(t.rcs) == 3
   assert isinstance(t.rcs[0], RCexpression)
   assert t.rcs[0].operator == 'and'
   assert isinstance(t.rcs[1], RC)
   assert isinstance(t.rcs[2], RC)
   assert t.rcs[0] is rcsA
   assert t.rcs[1] is rc3
   assert t.rcs[2] is rc4


def test_rc_operator_mixed_03( ):
   '''Operators combined.'''

   t = (RC(2, 0) ^ RC(3, 0)) | RC(3,0)

   assert isinstance(t, RCexpression)
   assert len(t.rcs) == 2
   assert isinstance(t.rcs[0], RCexpression)
   assert t.rcs[0].operator == 'xor'
   assert isinstance(t.rcs[1], RC)
   assert t.get_boolean_train(6) == [1,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_rc_operator_mixed_04( ):
   '''Operators combined.'''

   t = (RC(2, 0) ^ RC(3, 0)) | RC(3,0)

   assert isinstance(t, RCexpression)
   assert len(t.rcs) == 2
   assert isinstance(t.rcs[0], RCexpression)
   assert t.rcs[0].operator == 'xor'
   assert isinstance(t.rcs[1], RC)
   assert t.get_boolean_train(6) == [1,0,1,1,1,0]
   assert t.get_congruent_bases(6) == [0,2,3,4,6]






