from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools import componenttools
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval


def transpose_pitch_carrier_by_melodic_chromatic_interval(pitch_carrier, melodic_chromatic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by `melodic_chromatic_interval`. ::

      abjad> pitch = NamedChromaticPitch(12)
      abjad> mci = pitchtools.MelodicChromaticInterval(-3)
      abjad> pitchtools.transpose_pitch_carrier_by_melodic_chromatic_interval(pitch, mci)
      NamedChromaticPitch(a, 4)

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.transpose_by_melodic_chromatic_interval( )`` to
      ``pitchtools.transpose_pitch_carrier_by_melodic_chromatic_interval( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.transpose_pitch_by_melodic_chromatic_interval( )`` to
      ``pitchtools.transpose_pitch_carrier_by_melodic_chromatic_interval( )``.
   '''
   
   if not isinstance(melodic_chromatic_interval, MelodicChromaticInterval):
      raise TypeError('must be melodic chromatic interval.')
   
   if isinstance(pitch_carrier, NamedChromaticPitch):
      return NamedChromaticPitch(
         pitch_carrier.numbered_chromatic_pitch._chromatic_pitch_number + 
         melodic_chromatic_interval.number)
   elif isinstance(pitch_carrier, Note):
      new_note = componenttools.clone_components_and_remove_all_spanners([pitch_carrier])[0]
      new_pitch = NamedChromaticPitch(
         pitch_carrier.pitch.numbered_chromatic_pitch._chromatic_pitch_number + melodic_chromatic_interval.number)
      new_note.pitch = new_pitch
      return new_note
   elif isinstance(pitch_carrier, Chord):
      new_chord = componenttools.clone_components_and_remove_all_spanners([pitch_carrier])[0]
      for new_nh, old_nh in zip(
         new_chord.note_heads, pitch_carrier.note_heads):
         new_pitch = NamedChromaticPitch(
            old_nh.pitch.numbered_chromatic_pitch._chromatic_pitch_number + melodic_chromatic_interval.number)
         new_nh.pitch = new_pitch
      return new_chord
   else:
      raise TypeError('must be Abjad pitch, note or chord.')
