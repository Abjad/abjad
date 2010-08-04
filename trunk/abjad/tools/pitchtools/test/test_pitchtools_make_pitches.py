from abjad import *


def test_pitchtools_make_pitches_01( ):

   assert pitchtools.make_pitches([ ]) == [ ]
   assert pitchtools.make_pitches([0]) == [NamedPitch(0)]
   assert pitchtools.make_pitches([0, 2, 4]) == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]


def test_pitchtools_make_pitches_02( ):

   assert pitchtools.make_pitches([('df', 4)]) == [NamedPitch('df', 4)]
   assert pitchtools.make_pitches([NamedPitch('df', 4)]) == [NamedPitch('df', 4)]
   assert pitchtools.make_pitches([('df', 4), 0]) == [NamedPitch('df', 4), NamedPitch(0)]
