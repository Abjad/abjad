from abjad.helpers.is_less_than_voice import _is_less_than_voice
from abjad import *


def test_is_less_than_voice_01( ):

   assert _is_less_than_voice(Note(0, (1, 8)))
   assert _is_less_than_voice(FixedDurationTuplet((2, 8), scale(3)))
   assert _is_less_than_voice(FixedMultiplierTuplet((2, 3), scale(3)))
   assert _is_less_than_voice(RigidMeasure((3, 8), scale(3)))
   assert _is_less_than_voice(Container(scale(3)))
   assert not _is_less_than_voice(Voice(scale(3)))
   assert not _is_less_than_voice(Staff(scale(3)))
   assert not _is_less_than_voice(StaffGroup(Staff(scale(3)) * 2))
   assert not _is_less_than_voice(Score([Staff(scale(3))]))
