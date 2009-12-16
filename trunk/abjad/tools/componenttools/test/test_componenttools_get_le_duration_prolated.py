from abjad import *


def test_componenttools_get_le_duration_prolated_01( ):
   '''Accumulate maximum number of components from list 
   such that prolated duration of components is no greater
   than prolated duration at input.
   '''

   t = Voice(construct.scale(4))
   components, duration = componenttools.get_le_duration_prolated(
      t[:], Rational(1, 4))

   assert components == t[:2]
   assert duration == Rational(2, 8)


def test_componenttools_get_le_duration_prolated_02( ):

   t = Voice(construct.scale(4))
   components, duration = componenttools.get_le_duration_prolated(
      t[:], Rational(99))

   assert components == t[:]
   assert duration == Rational(4, 8) 
   

def test_componenttools_get_le_duration_prolated_03( ):

   t = Voice(construct.scale(4))
   components, duration = componenttools.get_le_duration_prolated(
      t[:], Rational(0))

   assert components == [ ]
   assert duration == Rational(0)


def test_componenttools_get_le_duration_prolated_04( ):

   t = Voice(construct.scale(4))
   components, duration = componenttools.get_le_duration_prolated(
      t[:], Rational(3, 16))

   assert components == t[:1]
   assert duration == Rational(1, 8)
