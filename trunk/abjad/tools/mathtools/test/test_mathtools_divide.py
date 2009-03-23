#from abjad.tools import mathtools
from abjad.rational.rational import Rational
import py.test


py.test.skip('New imports module raising ImportError.')

def test_mathtools_divide_01( ):
   '''
   Divide can take integers.
   '''
   t = mathtools.divide(1, [1,1,2])
   assert len(t) == 3
   assert t[0] == 1 / 4.
   assert t[1] == 1 / 4.
   assert t[2] == 1 / 2.


def test_mathtools_divide_02( ):
   '''
   Divide can take rationals.
   '''
   t = mathtools.divide(Rational(1, 2), [1,1,2])
   assert len(t) == 3
   assert t[0] == Rational(1, 8)
   assert t[1] == Rational(1, 8)
   assert t[2] == Rational(1, 4)
