from abjad.components import Chord
from abjad.components import Note
from abjad.tools import componenttools
from abjad.tools.pitchtools._Pitch import _Pitch
from abjad.tools.pitchtools.MelodicChromaticInterval import MelodicChromaticInterval
from abjad.tools.pitchtools.NamedChromaticPitch import NamedChromaticPitch


def transpose_pitch_carrier_by_melodic_chromatic_interval(
   pitch_carrier, melodic_chromatic_interval):
   '''.. versionadded:: 1.1.2

   Transpose `pitch_carrier` by `melodic_chromatic_interval`::

      abjad> pitch = NamedChromaticPitch(12)
      abjad> mci = pitchtools.MelodicChromaticInterval(-3)
      abjad> pitchtools.transpose_pitch_carrier_by_melodic_chromatic_interval(pitch, mci)
      NamedChromaticPitch(a, 4)
   
   Return new `pitch_carrier` type object.
   '''
   
   try:
      melodic_chromatic_interval = MelodicChromaticInterval(melodic_chromatic_interval)
   except (TypeError, ValueError):
      raise TypeError('must be melodic chromatic interval.')
      
   ## works for named & numbered pitches both chromatic & diatonic
   if isinstance(pitch_carrier, _Pitch):
      return type(pitch_carrier)(pitch_carrier.chromatic_pitch_number + 
         melodic_chromatic_interval.semitones)
   elif isinstance(pitch_carrier, Note):
      new_note = componenttools.clone_components_and_remove_all_spanners([pitch_carrier])[0]
      new_pitch = NamedChromaticPitch(
         abs(pitch_carrier.pitch.numbered_chromatic_pitch) + melodic_chromatic_interval.number)
      new_note.pitch = new_pitch
      return new_note
   elif isinstance(pitch_carrier, Chord):
      new_chord = componenttools.clone_components_and_remove_all_spanners([pitch_carrier])[0]
      for new_nh, old_nh in zip(new_chord.note_heads, pitch_carrier.note_heads):
         new_pitch = NamedChromaticPitch(
            abs(old_nh.pitch.numbered_chromatic_pitch) + melodic_chromatic_interval.number)
         new_nh.pitch = new_pitch
      return new_chord
   else:
      raise TypeError('must be Abjad pitch, note or chord.')
