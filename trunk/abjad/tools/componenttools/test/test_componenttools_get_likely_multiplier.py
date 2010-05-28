from abjad import *


def test_componenttools_get_likely_multiplier_01( ):
   '''Components were likely multiplied by 5/4.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(5, 4)) 
   assert componenttools.get_likely_multiplier(t[:]) == Rational(5, 4)


def test_componenttools_get_likely_multiplier_02( ):
   '''Components were likely multiplied by 3/2.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(3, 2)) 
   assert componenttools.get_likely_multiplier(t[:]) == Rational(3, 2)


def test_componenttools_get_likely_multiplier_03( ):
   '''Components were likely multiplied by 7/4.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(7, 4)) 
   assert componenttools.get_likely_multiplier(t[:]) == Rational(7, 4)


def test_componenttools_get_likely_multiplier_04( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(2)) 
   assert componenttools.get_likely_multiplier(t[:]) == Rational(1)


def test_componenttools_get_likely_multiplier_05( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(1, 2)) 
   assert componenttools.get_likely_multiplier(t[:]) == Rational(1)


def test_componenttools_get_likely_multiplier_06( ):
   '''Components multiplier recoverable only to within one power of two.'''

   t = Staff(construct.scale(4))
   containertools.contents_scale(t, Rational(10, 4)) 
   assert not componenttools.get_likely_multiplier(t[:]) == Rational(10, 4)
   assert componenttools.get_likely_multiplier(t[:]) == Rational(5, 4)


def test_componenttools_get_likely_multiplier_07( ):
   '''Return none when more than one likely multiplier.'''

   t = Staff(construct.notes([0], [(1, 8), (7, 32)]))
   assert componenttools.get_likely_multiplier(t[:]) is None
