from abjad import *


def test_RCexpression___init__01( ):
   '''Init sieve from rc instances and operator keyword.'''

   rcs = [ ]
   rcs.append(sievetools.RC(6, 0))
   rcs.append(sievetools.RC(6, 1))
   rcs.append(sievetools.RC(6, 4))
   sieve = sievetools.RCexpression(rcs, operator = 'or')

   assert isinstance(sieve, sievetools.RCexpression)
   assert sieve.rcs == rcs
   assert sieve.operator == 'or'


def test_RCexpression___init__02( ):
   '''Init sieve from other sieve instance.'''

   rcs = [ ]
   rcs.append(sievetools.RC(6, 0))
   rcs.append(sievetools.RC(6, 1))
   rcs.append(sievetools.RC(6, 4))
   sieve = sievetools.RCexpression(sievetools.RCexpression(rcs, operator = 'or'))

   assert isinstance(sieve, sievetools.RCexpression)
   assert sieve.rcs == rcs
   assert sieve.operator == 'or'
