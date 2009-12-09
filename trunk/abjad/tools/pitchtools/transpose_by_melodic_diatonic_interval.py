from abjad.chord import Chord
from abjad.note import Note
from abjad.pitch import Pitch
from abjad.tools import clone
from abjad.tools.pitchtools.MelodicDiatonicInterval import \
   MelodicDiatonicInterval
from abjad.tools.pitchtools.diatonic_scale_degree_to_letter import \
   diatonic_scale_degree_to_letter


def transpose_by_melodic_diatonic_interval(
   pitch_carrier, melodic_diatonic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by `melodic_diatonic_interval`. ::

      abjad> pitch = Pitch(12)
      abjad> mdi = pitchtools.MelodicDiatonicInterval('minor', -3)
      abjad> pitchtools.transpose_by_melodic_diatonic_interval(pitch, mdi)
      Pitch(a, 4)
   '''

   if not isinstance(melodic_diatonic_interval, MelodicDiatonicInterval):
      raise TypeError('must be melodic diatonic interval.')

   if isinstance(pitch_carrier, Pitch):
      return _transpose_pitch_by_melodic_diatonic_interval(
         pitch_carrier, melodic_diatonic_interval)
   elif isinstance(pitch_carrier, Note):
      new_note = clone.unspan([pitch_carrier])[0]
      new_pitch = _transpose_pitch_by_melodic_diatonic_interval(
         pitch_carrier.pitch, melodic_diatonic_interval)
      new_note.pitch = new_pitch
      return new_note
   elif isinstance(pitch_carrier, Chord):
      new_chord = clone.unspan([pitch_carrier])[0]
      for new_nh, old_nh in zip(
         new_chord.note_heads, pitch_carrier.note_heads):
         new_pitch = _transpose_pitch_by_melodic_diatonic_interval(
            old_nh.pitch, melodic_diatonic_interval)
         new_nh.pitch = new_pitch
      return new_chord
   else:
      raise TypeError('must be pitch, note or chord.')


def _transpose_pitch_by_melodic_diatonic_interval(
   pitch, melodic_diatonic_interval):
   if not isinstance(pitch, Pitch):
      raise TypeError('must be pitch.')
   chromatic_pitch_number = pitch.number + melodic_diatonic_interval.semitones
   diatonic_scale_degree = pitch.degree + melodic_diatonic_interval.staff_spaces
   letter = diatonic_scale_degree_to_letter(diatonic_scale_degree)
   return Pitch(chromatic_pitch_number, letter)
