from abjad import *


def test_PitchClassSet___init___01( ):
   '''Works with numbers.'''

   assert len(pitchtools.PitchClassSet([0, 2, 6, 7])) == 4


def test_PitchClassSet___init___02( ):
   '''Works with pitch classes.'''

   assert len(pitchtools.PitchClassSet(
      [pitchtools.PitchClass(x) for x in [0, 2, 6, 7]])) == 4


def test_PitchClassSet___init___03( ):
   '''Works with chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   pitch_class_set = pitchtools.PitchClassSet(chord)
   assert len(pitch_class_set) == 3


def test_PitchClassSet___init___04( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   pitch_class_set = pitchtools.PitchClassSet(note)
   assert len(pitch_class_set) == 1
