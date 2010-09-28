from abjad import *


def test_componenttools_get_likely_multiplier_of_components_01( ):
   '''Components were likely multiplied by 5/4.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(5, 4)) 
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(5, 4)


def test_componenttools_get_likely_multiplier_of_components_02( ):
   '''Components were likely multiplied by 3/2.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(3, 2)) 
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(3, 2)


def test_componenttools_get_likely_multiplier_of_components_03( ):
   '''Components were likely multiplied by 7/4.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(7, 4)) 
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(7, 4)


def test_componenttools_get_likely_multiplier_of_components_04( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(2)) 
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(1)


def test_componenttools_get_likely_multiplier_of_components_05( ):
   '''Components likely multiplier not recoverable.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(1, 2)) 
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(1)


def test_componenttools_get_likely_multiplier_of_components_06( ):
   '''Components multiplier recoverable only to within one power of two.'''

   t = Staff(macros.scale(4))
   containertools.scale_contents_of_container(t, Fraction(10, 4)) 
   assert not componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(10, 4)
   assert componenttools.get_likely_multiplier_of_components(t[:]) == Fraction(5, 4)


def test_componenttools_get_likely_multiplier_of_components_07( ):
   '''Return none when more than one likely multiplier.'''

   t = Staff(notetools.make_notes([0], [(1, 8), (7, 32)]))
   assert componenttools.get_likely_multiplier_of_components(t[:]) is None
