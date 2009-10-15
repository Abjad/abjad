from abjad.tools.pitchtools.get_pitch import get_pitch
from abjad.tools.pitchtools.PitchClass import PitchClass


def get_pitch_class(pitch_carrier):
   '''.. versionadded:: 1.1.2

   Get pitch class from `pitch_carrier`. ::

      abjad> note = Note(13, (1, 4))
      abjad> pitchtools.get_pitch_class(note)
      PitchClass(1)

   One-note chords work fine. ::

      abjad> one_note_chord = Chord([13], (1, 4))
      abjad> pitchtools.get_pitch_class(one_note_chord)
      PitchClass(1)

   Empty chords Raise :exc:`MissingPitchError`. ::

      abjad> empty_chord = Chord([], (1, 4))
      abjad> pitchtools.get_pitch_class(empty_chord)
      MissingPitchError

   Many-note chords raise :exc:`ExtraPitchError`. ::

      abjad> chord = Chord([13, 23, 24], (1, 4))
      abjad> pitchtools.get_pitch_class(chord)
      ExtraPitchError
   '''

   pitch = get_pitch(pitch_carrier)
   pitch_class = PitchClass(pitch)
   return pitch_class
