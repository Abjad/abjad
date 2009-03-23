#from abjad.tools import mathtools
#from abjad.rational.rational import Rational
#import py.test
#
#py.test.skip('Why does abjad.tools import mathtools not work inside a script?')
#
#def test_mathtools_fragment_01( ):
#   '''
#   fragment can take integers.
#   '''
#   t = mathtools.fragment(4, [1,2])
#   assert len(t) == 3
#   assert t[0] == 1
#   assert t[1] == 2
#   assert t[2] == 1
#
#
#def test_mathtools_fragment_02( ):
#   '''
#   fragment can take floats.
#   '''
#   t = mathtools.fragment(4, [0.5, 2])
#   assert len(t) == 3
#   assert t[0] == 0.5
#   assert t[1] == 2
#   assert t[2] == 1.5
#
#
#def test_mathtools_fragment_03( ):
#   '''
#   fragment can take rationals.
#   '''
#   t = mathtools.fragment(1, [Rational(1, 2), Rational(1, 3)])
#   assert len(t) == 3
#   assert t[0] == Rational(1, 2)
#   assert t[1] == Rational(1, 3)
#   assert t[2] == Rational(1, 6)
#
#
#### ERRORS ###
#
#def test_mathtools_fragment_05( ):
#   '''
#   The sum of the fragments must be smaller than the total to be fragmented.
#   '''
#   assert py.test.raises(AssertionError, 'mathtools.fragment(1, [2])')   
#
