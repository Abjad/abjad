from abjad import *


def test_pitchtools_make_pitches_01( ):

   assert pitchtools.make_pitches([ ]) == [ ]
   assert pitchtools.make_pitches([0]) == [Pitch(0)]
   assert pitchtools.make_pitches([0, 2, 4]) == [Pitch(0), Pitch(2), Pitch(4)]


def test_pitchtools_make_pitches_02( ):

   assert pitchtools.make_pitches([('df', 4)]) == [Pitch('df', 4)]
   assert pitchtools.make_pitches([Pitch('df', 4)]) == [Pitch('df', 4)]
   assert pitchtools.make_pitches([('df', 4), 0]) == [Pitch('df', 4), Pitch(0)]
