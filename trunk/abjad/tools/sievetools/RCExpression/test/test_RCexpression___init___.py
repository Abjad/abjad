from abjad import *


def test_RCexpression___init____01( ):
   '''Init sieve from rc instances and operator keyword.'''

   rcs = [ ]
   rcs.append(sievetools.RC(6, 0))
   rcs.append(sievetools.RC(6, 1))
   rcs.append(sievetools.RC(6, 4))
   sieve = sievetools.RCExpression(rcs, operator = 'or')

   assert isinstance(sieve, sievetools.RCExpression)
   assert sieve.rcs == rcs
   assert sieve.operator == 'or'


def test_RCexpression___init____02( ):
   '''Init sieve from other sieve instance.'''

   rcs = [ ]
   rcs.append(sievetools.RC(6, 0))
   rcs.append(sievetools.RC(6, 1))
   rcs.append(sievetools.RC(6, 4))
   sieve = sievetools.RCExpression(sievetools.RCExpression(rcs, operator = 'or'))

   assert isinstance(sieve, sievetools.RCExpression)
   assert sieve.rcs == rcs
   assert sieve.operator == 'or'
