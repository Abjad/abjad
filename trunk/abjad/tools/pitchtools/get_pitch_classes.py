from abjad.tools.pitchtools.get_pitches import get_pitches
from abjad.tools.pitchtools.NumericPitchClass import NumericPitchClass


def get_pitch_classes(expr):
   '''.. versionadded:: 1.1.2

   Get tuple of zero or more pitch classes from almost
   any expression `expr`.

   Works with notes. ::

      abjad> note = Note(13, (1, 4))
      abjad> pitchtools.get_pitch_classes(note)
      (NumerciPitchClass(1),)

   Works with multiple-note chords. ::

      abjad> chord = Chord([13, 14, 15], (1, 4))
      abjad> pitchtools.get_pitch_classes(chord)
      (NumerciPitchClass(1), NumericPitchClass(2), NumericPitchClass(3))

   Works with empty chords. ::

      abjad> empty_chord = Chord([ ], (1, 4))
      abjad> pitchtools.get_pitch_classes(empty_chord)
      ()

   Works with one-note chords. ::

      abjad> one_note_chord = Chord([13], (1, 4))
      abjad> pitchtools.get_pitch_classes(one_note_chord)
      (NumericPitchClass(1),)
   '''

   pitches = get_pitches(expr)
   pitch_classes = [NumericPitchClass(pitch) for pitch in pitches]
   pitch_classes = tuple(pitch_classes)
   return pitch_classes
