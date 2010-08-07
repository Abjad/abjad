from abjad import *


def test_pitchtools_get_pitch_classes_01( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   assert pitchtools.get_pitch_classes(note) == (pitchtools.NumericPitchClass(1), )


def test_pitchtools_get_pitch_classes_02( ):
   '''Works with multiple-note chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   assert pitchtools.get_pitch_classes(chord) == (
      pitchtools.NumericPitchClass(1),
      pitchtools.NumericPitchClass(2),
      pitchtools.NumericPitchClass(3))


def test_pitchtools_get_pitch_classes_03( ):
   '''Works with one-note chords.'''

   chord = Chord([13], (1, 4))
   assert pitchtools.get_pitch_classes(chord) == (pitchtools.NumericPitchClass(1), )


def test_pitchtools_get_pitch_classes_04( ):
   '''Works with empty chords.'''

   chord = Chord([ ], (1, 4))
   assert pitchtools.get_pitch_classes(chord) == ( )
