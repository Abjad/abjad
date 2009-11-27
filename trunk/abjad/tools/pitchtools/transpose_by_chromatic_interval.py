from ChromaticInterval import ChromaticInterval
from abjad.chord import Chord
from abjad.note import Note
from abjad.pitch import Pitch
from abjad.tools import clone


def transpose_by_chromatic_interval(pitch_carrier, chromatic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by `chromatic_interval`. ::

      abjad> pitch = Pitch(12)
      abjad> chromatic_interval = pitchtools.ChromaticInterval(-3)
      abjad> pitchtools.transpose_by_chromatic_interval(pitch, chromatic_interval)
      Pitch(a, 4)
   '''
   
   if not isinstance(chromatic_interval, ChromaticInterval):
      raise TypeError('must be chromatic interval.')
   
   if isinstance(pitch_carrier, Pitch):
      return Pitch(pitch_carrier.number + chromatic_interval.interval_number)
   elif isinstance(pitch_carrier, Note):
      new_note = clone.unspan([pitch_carrier])[0]
      new_pitch = Pitch(
         pitch_carrier.pitch.number + chromatic_interval.interval_number)
      new_note.pitch = new_pitch
      return new_note
   elif isinstance(pitch_carrier, Chord):
      new_chord = clone.unspan([pitch_carrier])[0]
      for new_nh, old_nh in zip(
         new_chord.note_heads, pitch_carrier.note_heads):
         new_pitch = Pitch(
            old_nh.pitch.number + chromatic_interval.interval_number)
         new_nh.pitch = new_pitch
      return new_chord
   else:
      raise TypeError('must be Abjad pitch, note or chord.')
