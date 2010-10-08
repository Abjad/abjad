from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.pitchtools.NumberedChromaticPitchClass import NumberedChromaticPitchClass


def get_numeric_chromatic_pitch_class_from_pitch_carrier(pitch_carrier):
   '''.. versionadded:: 1.1.2

   Get pitch class from `pitch_carrier`. ::

      abjad> note = Note(13, (1, 4))
      abjad> pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier(note)
      NumberedChromaticPitchClass(1)

   One-note chords work fine. ::

      abjad> one_note_chord = Chord([13], (1, 4))
      abjad> pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier(one_note_chord)
      NumberedChromaticPitchClass(1)

   Empty chords Raise :exc:`MissingPitchError`. ::

      abjad> empty_chord = Chord([ ], (1, 4))
      abjad> pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier(empty_chord)
      MissingPitchError

   Many-note chords raise :exc:`ExtraPitchError`. ::

      abjad> chord = Chord([13, 23, 24], (1, 4))
      abjad> pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier(chord)
      ExtraPitchError

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_named_chromatic_pitch_from_pitch_carrier_class( )`` to
      ``pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_numbered_chromatic_pitch_class_from_pitch_carrier( )`` to
      ``pitchtools.get_numeric_chromatic_pitch_class_from_pitch_carrier( )``.
   '''

   pitch = get_named_chromatic_pitch_from_pitch_carrier(pitch_carrier)
   pitch_class = NumberedChromaticPitchClass(pitch)
   return pitch_class
