from abjad.tools.pitchtools.list_named_chromatic_pitches_in_expr import list_named_chromatic_pitches_in_expr
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass


def list_numeric_chromatic_pitch_classes_in_expr(expr):
   '''.. versionadded:: 1.1.2

   Get tuple of zero or more pitch classes from almost
   any expression `expr`.

   Works with notes. ::

      abjad> note = Note(13, (1, 4))
      abjad> pitchtools.list_numeric_chromatic_pitch_classes_in_expr(note)
      (NumerciPitchClass(1),)

   Works with multiple-note chords. ::

      abjad> chord = Chord([13, 14, 15], (1, 4))
      abjad> pitchtools.list_numeric_chromatic_pitch_classes_in_expr(chord)
      (NumerciPitchClass(1), NumberedChromaticPitchClass(2), NumberedChromaticPitchClass(3))

   Works with empty chords. ::

      abjad> empty_chord = Chord([ ], (1, 4))
      abjad> pitchtools.list_numeric_chromatic_pitch_classes_in_expr(empty_chord)
      ( )

   Works with one-note chords. ::

      abjad> one_note_chord = Chord([13], (1, 4))
      abjad> pitchtools.list_numeric_chromatic_pitch_classes_in_expr(one_note_chord)
      (NumberedChromaticPitchClass(1),)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrieres( )`` to
      ``pitchtools.list_numeric_chromatic_pitch_classes_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.list_numeric_pitch_classes_in_expr( )`` to
      ``pitchtools.list_numeric_chromatic_pitch_classes_in_expr( )``.
   '''

   pitches = list_named_chromatic_pitches_in_expr(expr)
   pitch_classes = [NumberedChromaticPitchClass(pitch) for pitch in pitches]
   pitch_classes = tuple(pitch_classes)
   return pitch_classes
