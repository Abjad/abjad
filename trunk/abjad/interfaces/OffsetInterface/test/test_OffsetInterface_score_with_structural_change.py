from abjad import *


## TODO: Write a good 6 or 8 offset interface with structural change tests ##

def test_OffsetInterface_score_with_structural_change_01( ):
   '''Insert note in voice.'''

   t = Voice(macros.scale(4))
   Beam(t[:])
   note = t[2]
   assert note.offset.prolated.start == Rational(1, 4)

   t.insert(2, Note(3, (1, 8)))
   assert note.offset.prolated.start == Rational(3, 8)


def test_OffsetInterface_score_with_structural_change_02( ):
   '''Delete note in voice.'''

   t = Voice(macros.scale(4))
   Beam(t[:])
   note = t[2]
   assert note.offset.prolated.start == Rational(1, 4)

   del(t[1])
   assert note.offset.prolated.start == Rational(1, 8)
