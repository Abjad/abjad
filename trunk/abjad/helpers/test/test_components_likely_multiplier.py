from abjad import *
from abjad.helpers.components_likely_multiplier import _components_likely_multiplier
from abjad.tools import construct


def test_components_likely_multiplier_01( ):
   '''Components were likely multiplier by 5/4.'''

   t = Staff(scale(4))
   container_scale(t, Rational(5, 4)) 
   assert _components_likely_multiplier(t[:]) == Rational(5, 4)


def test_components_likely_multiplier_02( ):
   '''Components were likely multiplier by 3/2.'''

   t = Staff(scale(4))
   container_scale(t, Rational(3, 2)) 
   assert _components_likely_multiplier(t[:]) == Rational(3, 2)


def test_components_likely_multiplier_03( ):
   '''Components were likely multiplier by 4/4.'''

   t = Staff(scale(4))
   container_scale(t, Rational(7, 4)) 
   assert _components_likely_multiplier(t[:]) == Rational(7, 4)


def test_components_likely_multiplier_04( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(scale(4))
   container_scale(t, Rational(2)) 
   assert _components_likely_multiplier(t[:]) == Rational(1)


def test_components_likely_multiplier_05( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(scale(4))
   container_scale(t, Rational(1, 2)) 
   assert _components_likely_multiplier(t[:]) == Rational(1)


def test_components_likely_multiplier_06( ):
   '''Components multiplier recoverable only to within one power of two.'''

   t = Staff(scale(4))
   container_scale(t, Rational(10, 4)) 
   assert not _components_likely_multiplier(t[:]) == Rational(10, 4)
   assert _components_likely_multiplier(t[:]) == Rational(5, 4)
