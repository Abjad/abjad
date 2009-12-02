from abjad import *


def test_pitchtools_PitchSet___init___01( ):
   '''Works with numbers.'''

   assert len(pitchtools.PitchSet([12, 14, 18, 19])) == 4


def test_pitchtools_PitchSet___init___02( ):
   '''Works with pitches.'''

   assert len(pitchtools.PitchSet([Pitch(x) for x in [12, 14, 18, 19]])) == 4


def test_pitchtools_PitchSet___init___03( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   pitch_set = pitchtools.PitchSet(pitchtools.get_pitches(note))
   assert len(pitch_set) == 1


def test_pitchtools_PitchSet___init___04( ):
   '''Works with chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   pitch_set = pitchtools.PitchSet(pitchtools.get_pitches(chord))
   assert len(pitch_set) == 3


def test_pitchtools_PitchSet___init___05( ):
   '''Works with chords with duplicate pitches.'''

   chord = Chord([13, 13, 13, 14], (1, 4))
   pitch_set = pitchtools.PitchSet(pitchtools.get_pitches(chord))
   assert len(pitch_set) == 2


def test_pitchtools_PitchSet___init___06( ):
   '''Works with empty chords.'''

   chord = Note([ ], (1, 4))
   pitch_set = pitchtools.PitchSet(pitchtools.get_pitches(chord))
   assert len(pitch_set) == 0
