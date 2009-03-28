from abjad import *


def test_get_components_le_prolated_duration_01( ):
   '''Accumulate components from list.
      Stop when total prolated duration *just* <= 'prolated_duration'.
      Return (accumulated components, accumulated duration).'''

   t = Voice(scale(4))
   components, duration = get_components_le_prolated_duration(
      t[:], Rational(1, 4))

   assert components == t[:2]
   assert duration == Rational(2, 8)


def test_get_components_le_prolated_duration_02( ):

   t = Voice(scale(4))
   components, duration = get_components_le_prolated_duration(
      t[:], Rational(99))

   assert components == t[:]
   assert duration == Rational(4, 8) 
   

def test_get_components_le_prolated_duration_03( ):

   t = Voice(scale(4))
   components, duration = get_components_le_prolated_duration(
      t[:], Rational(0))

   assert components == [ ]
   assert duration == Rational(0)


def test_get_components_le_prolated_duration_04( ):

   t = Voice(scale(4))
   components, duration = get_components_le_prolated_duration(
      t[:], Rational(3, 16))

   assert components == t[:1]
   assert duration == Rational(1, 8)
