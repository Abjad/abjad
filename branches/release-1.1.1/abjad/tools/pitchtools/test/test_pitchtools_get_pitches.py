from abjad import *


def test_pitchtools_get_pitches_01( ):

   tuplet = FixedDurationTuplet((2, 8), construct.scale(3))
   t = pitchtools.get_pitches(tuplet)

   assert t == (Pitch('c', 4), Pitch('d', 4), Pitch('e', 4))


def test_pitchtools_get_pitches_02( ):

   staff = Staff(construct.scale(4))
   beam = Beam(staff[:])
   t = pitchtools.get_pitches(beam)

   assert t == (Pitch('c', 4), Pitch('d', 4), Pitch('e', 4), Pitch('f', 4))
