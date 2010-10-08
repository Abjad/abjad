from abjad.components.Chord import Chord
from abjad.components.Note import Note
from abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch import NamedChromaticPitch
from abjad.tools.pitchtools.MelodicDiatonicInterval import MelodicDiatonicInterval


def set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(expr, key_signature = None):
   r'''Apply ascending diatonic pitches to the notes
   and chords in `expr`. ::

      abjad> staff = Staff(notetools.make_notes(0, [(5, 32)] * 4))
      abjad> macros.diatonicize(staff)
      abjad> f(staff)
      \new Staff {
         c'8 ~
         c'32
         d'8 ~
         d'32
         e'8 ~
         e'32
         f'8 ~
         f'32
      }

   Used primarily in generating test file examples.

   .. versionadded:: 1.1.2
      Optional `key_signature` keyword argument.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.diatonicize( )`` to
      ``macros.diatonicize( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr( )`` to
      ``pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr( )``.
   '''
   from abjad.tools import tietools
   from abjad.tools import tonalitytools

   #diatonic_residues = (0, 2, 4, 5, 7, 9, 11)
   #length = len(diatonic_residues)

   if key_signature is None:
      scale = tonalitytools.Scale('C', 'major')
   else:
      scale = tonalitytools.Scale(key_signature)

   dicg = scale.diatonic_interval_class_segment
   length = len(dicg)

   octave_number = 4
   pitch = NamedChromaticPitch(scale[0], octave_number)

   for i, tie_chain in enumerate(tietools.iterate_tie_chains_forward_in_expr(expr)):
      #pitch = int(i / length) * 12 + diatonic_residues[i % length] 
      #named_pitch_class = scale[i % length]
      #pitch_class_number = named_pitch_class.pitch_class.number
      #pitch_number = int(i / length) * 12 + pitch_class_number
      #pitch = NamedChromaticPitch(pitch_number, named_pitch_class)
      if isinstance(tie_chain[0], Note):
         for note in tie_chain:
            note.pitch = pitch
      elif isinstance(tie_chain[0], Chord):
         for chord in tie_chain:
            chord.pitches = [pitch]
      else:
         pass
      dic = dicg[i % length]
      ascending_mdi = MelodicDiatonicInterval(dic.quality_string, dic.number)
      pitch += ascending_mdi
