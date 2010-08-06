from abjad import *


def test_leaftools_copy_written_duration_and_multiplier_from_leaf_to_leaf_01( ):

   note = Note(0, (1, 4))
   note.duration.multiplier = Rational(1, 2)
   rest = Rest((1, 64))

   leaftools.copy_written_duration_and_multiplier_from_leaf_to_leaf(note, rest)

   assert note.duration.written == Rational(1, 4)
   assert note.duration.multiplier == Rational(1, 2)

   assert rest.duration.written == Rational(1, 4)
   assert rest.duration.multiplier == Rational(1, 2)
