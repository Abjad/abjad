from abjad.leaf import _Leaf
from abjad.pitch import Pitch
from abjad.tools import iterate
from abjad.tools.pitchtools.pitch_number_to_octave import \
   pitch_number_to_octave as pitchtools_pitch_number_to_octave
from abjad.tools.pitchtools.pc_to_pitch_name_sharps import \
   pc_to_pitch_name_sharps as pitchtools_pc_to_pitch_name_sharps


def make_sharp(expr):

   if isinstance(expr, Pitch):
      _pitch_renotate_sharps(expr)
   else:
      for leaf in iterate.naive_forward(expr, _Leaf):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_sharps(pitch)


def _pitch_renotate_sharps(pitch):
   octave = pitchtools_pitch_number_to_octave(pitch.number)
   name = pitchtools_pc_to_pitch_name_sharps(pitch.pc)
   pitch.octave = octave
   pitch.name = name
