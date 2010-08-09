from abjad import *


def test_pitchtools_list_numeric_pitch_classes_in_expr_01( ):
   '''Works with notes.'''

   note = Note(13, (1, 4))
   assert pitchtools.list_numeric_pitch_classes_in_expr(note) == (pitchtools.NumericPitchClass(1), )


def test_pitchtools_list_numeric_pitch_classes_in_expr_02( ):
   '''Works with multiple-note chords.'''

   chord = Chord([13, 14, 15], (1, 4))
   assert pitchtools.list_numeric_pitch_classes_in_expr(chord) == (
      pitchtools.NumericPitchClass(1),
      pitchtools.NumericPitchClass(2),
      pitchtools.NumericPitchClass(3))


def test_pitchtools_list_numeric_pitch_classes_in_expr_03( ):
   '''Works with one-note chords.'''

   chord = Chord([13], (1, 4))
   assert pitchtools.list_numeric_pitch_classes_in_expr(chord) == (pitchtools.NumericPitchClass(1), )


def test_pitchtools_list_numeric_pitch_classes_in_expr_04( ):
   '''Works with empty chords.'''

   chord = Chord([ ], (1, 4))
   assert pitchtools.list_numeric_pitch_classes_in_expr(chord) == ( )
