from abjad.tools.pitchtools.NamedPitch.NamedPitch import NamedPitch
from abjad.tools import iterate
from abjad.tools.pitchtools.pitch_number_to_octave import pitch_number_to_octave as pitchtools_pitch_number_to_octave
from abjad.tools.pitchtools.pc_to_pitch_name_flats import pc_to_pitch_name_flats as pitchtools_pc_to_pitch_name_flats


def make_flat(expr):
   r'''Renotate every pitch in `expr` with zero or more flats.

   ::

      abjad> staff = Staff(leaftools.make_repeated_notes(6))
      abjad> pitchtools.set_ascending_chromatic_pitches_on_nontied_pitched_components_in_expr(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
         e'8
         f'8
      }
      abjad> pitchtools.make_flat(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         df'8
         d'8
         ef'8
         e'8
         f'8
      }
   '''


   if isinstance(expr, NamedPitch):
      _pitch_renotate_flats(expr)
   else:
      for leaf in iterate.leaves_forward_in_expr(expr):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_flats(pitch)


def _pitch_renotate_flats(pitch):
   octave = pitchtools_pitch_number_to_octave(pitch.number)
   name = pitchtools_pc_to_pitch_name_flats(pitch.pc)
   pitch.octave = octave
   pitch.name = name
