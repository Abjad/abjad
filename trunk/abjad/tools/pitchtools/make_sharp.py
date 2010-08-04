from abjad.NamedPitch import Pitch
from abjad.tools import iterate
from abjad.tools.pitchtools.pitch_number_to_octave import \
   pitch_number_to_octave as pitchtools_pitch_number_to_octave
from abjad.tools.pitchtools.pc_to_pitch_name_sharps import \
   pc_to_pitch_name_sharps as pitchtools_pc_to_pitch_name_sharps


def make_sharp(expr):
   r'''Renotate every pitch in `expr` with zero 
   or more sharps. ::

      abjad> staff = Staff(leaftools.make_repeated_notes(6))
      abjad> pitchtools.chromaticize(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ef'8
         e'8
         f'8
      }
      abjad> pitchtools.make_sharp(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         cs'8
         d'8
         ds'8
         e'8
         f'8
      }
   '''

   if isinstance(expr, Pitch):
      _pitch_renotate_sharps(expr)
   else:
      for leaf in iterate.leaves_forward_in_expr(expr):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_sharps(pitch)


def _pitch_renotate_sharps(pitch):
   octave = pitchtools_pitch_number_to_octave(pitch.number)
   name = pitchtools_pc_to_pitch_name_sharps(pitch.pc)
   pitch.octave = octave
   pitch.name = name
