from abjad import *


def test_pitchtools_is_carrier_01( ):

   assert pitchtools.is_carrier(Pitch(0))
   assert pitchtools.is_carrier(Note(0, (1, 4)))
   assert pitchtools.is_carrier(NoteHead(None, 0))
   assert pitchtools.is_carrier(Chord([0, 2, 11], (1, 4)))


def test_pitchtools_is_carrier_02( ):

   assert not pitchtools.is_carrier(Staff([ ]))
   assert not pitchtools.is_carrier(Voice([ ]))
   assert not pitchtools.is_carrier(0)
   assert not pitchtools.is_carrier('foo')
