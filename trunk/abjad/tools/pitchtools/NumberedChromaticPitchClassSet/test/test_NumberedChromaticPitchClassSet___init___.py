from abjad import *


def test_NumberedChromaticPitchClassSet___init____01( ):
   '''Works with numbers.'''

   assert len(pitchtools.NumberedChromaticPitchClassSet([0, 2, 6, 7])) == 4


def test_NumberedChromaticPitchClassSet___init____02( ):
   '''Works with pitch classes.'''

   assert len(pitchtools.NumberedChromaticPitchClassSet(
      [pitchtools.NumberedChromaticPitchClass(x) for x in [0, 2, 6, 7]])) == 4


def test_NumberedChromaticPitchClassSet___init____03( ):
   '''Works with chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   pitch_class_set = pitchtools.NumberedChromaticPitchClassSet(chord)
   assert len(pitch_class_set) == 3


def test_NumberedChromaticPitchClassSet___init____04( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   pitch_class_set = pitchtools.NumberedChromaticPitchClassSet(note)
   assert len(pitch_class_set) == 1
