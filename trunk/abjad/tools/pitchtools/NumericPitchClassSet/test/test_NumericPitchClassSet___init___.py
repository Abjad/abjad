from abjad import *


def test_NumericPitchClassSet___init____01( ):
   '''Works with numbers.'''

   assert len(pitchtools.NumericPitchClassSet([0, 2, 6, 7])) == 4


def test_NumericPitchClassSet___init____02( ):
   '''Works with pitch classes.'''

   assert len(pitchtools.NumericPitchClassSet(
      [pitchtools.NumericPitchClass(x) for x in [0, 2, 6, 7]])) == 4


def test_NumericPitchClassSet___init____03( ):
   '''Works with chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   pitch_class_set = pitchtools.NumericPitchClassSet(chord)
   assert len(pitch_class_set) == 3


def test_NumericPitchClassSet___init____04( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   pitch_class_set = pitchtools.NumericPitchClassSet(note)
   assert len(pitch_class_set) == 1
