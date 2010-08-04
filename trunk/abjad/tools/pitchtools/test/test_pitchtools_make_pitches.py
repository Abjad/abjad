from abjad import *


def test_pitchtools_make_pitches_01( ):

   assert pitchtools.make_pitches([ ]) == [ ]
   assert pitchtools.make_pitches([0]) == [pitchtools.NamedPitch(0)]
   assert pitchtools.make_pitches([0, 2, 4]) == [pitchtools.NamedPitch(0), pitchtools.NamedPitch(2), pitchtools.NamedPitch(4)]


def test_pitchtools_make_pitches_02( ):

   assert pitchtools.make_pitches([('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.make_pitches([pitchtools.NamedPitch('df', 4)]) == [pitchtools.NamedPitch('df', 4)]
   assert pitchtools.make_pitches([('df', 4), 0]) == [pitchtools.NamedPitch('df', 4), pitchtools.NamedPitch(0)]
