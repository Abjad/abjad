from abjad import *


def test_pitchtools_has_duplicate_pitch_01( ):
   '''Works with chords.'''

   assert pitchtools.has_duplicate_pitch(Chord([13, 13, 14], (1, 4)))
   assert not pitchtools.has_duplicate_pitch(Chord([13, 14], (1, 4)))
   assert not pitchtools.has_duplicate_pitch(Chord([ ], (1, 4)))


def test_pitchtools_has_duplicate_pitch_02( ):
   '''Works with notes, rests and skips.'''

   assert not pitchtools.has_duplicate_pitch(Note(13, (1, 4)))
   assert not pitchtools.has_duplicate_pitch(Rest((1, 4)))
   assert not pitchtools.has_duplicate_pitch(Skip((1, 4)))


def test_pitchtools_has_duplicate_pitch_03( ):
   '''Works with containers.'''

   staff = Staff(leaftools.make_repeated_notes(4))
   assert pitchtools.has_duplicate_pitch(staff)

   staff = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   assert not pitchtools.has_duplicate_pitch(staff)
