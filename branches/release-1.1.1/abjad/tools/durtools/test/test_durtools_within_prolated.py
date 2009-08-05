from abjad import *


def test_durtools_within_prolated_01( ):
   '''True when split point is within prolated duration of component.'''

   assert durtools.within_prolated(Rational(0), Note(0, (1, 4)))
   assert durtools.within_prolated(Rational(1, 16), Note(0, (1, 4)))
   assert durtools.within_prolated(Rational(1, 12), Note(0, (1, 4)))
   assert not durtools.within_prolated(Rational(1, 4), Note(0, (1, 4)))
