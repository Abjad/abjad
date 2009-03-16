from abjad.helpers.is_voice_guarantor import _is_voice_guarantor
from abjad import *


def test_is_voice_guarantor_01( ):
   '''True when expr is an Abjad context or parallel container,
      otherwise False.'''

   assert not _is_voice_guarantor(Container([ ]))
   assert not _is_voice_guarantor(FixedDurationTuplet((2, 8), [ ]))
   assert not _is_voice_guarantor(FixedMultiplierTuplet((2, 3), [ ]))
   assert _is_voice_guarantor(GrandStaff([ ]))
   assert _is_voice_guarantor(Parallel([ ]))
   assert _is_voice_guarantor(PianoStaff([ ]))
   assert _is_voice_guarantor(RhythmicSketchStaff([ ]))
   assert _is_voice_guarantor(RhythmicStaff([ ]))
   assert not _is_voice_guarantor(RigidMeasure((4, 8), [ ]))
   assert _is_voice_guarantor(Score([ ]))
   assert not _is_voice_guarantor(Sequential([ ]))
   assert _is_voice_guarantor(Staff([ ]))
   assert _is_voice_guarantor(StaffGroup([ ]))
   assert _is_voice_guarantor(Voice([ ]))


def test_is_voice_guarantor_02( ):
   '''True when expr is an Abjad context or parallel container,
      otherwise False.'''

   t = Container([ ])
   t.brackets = 'simultaneous'
   assert _is_voice_guarantor(t)

   t = Container([ ])
   t.brackets = 'double-angle'
   assert _is_voice_guarantor(t)
