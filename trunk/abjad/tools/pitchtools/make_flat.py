from abjad.pitch import Pitch
from abjad.tools import iterate
from abjad.tools.pitchtools.pitch_number_to_octave import \
   pitch_number_to_octave as pitchtools_pitch_number_to_octave
from abjad.tools.pitchtools.pc_to_pitch_name_flats import \
   pc_to_pitch_name_flats as pitchtools_pc_to_pitch_name_flats


def make_flat(expr):

   if isinstance(expr, Pitch):
      _pitch_renotate_flats(expr)
   else:
      for leaf in iterate.leaves_forward_in(expr):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_flats(pitch)


def _pitch_renotate_flats(pitch):
   #octave = pitch.tools.pitchNumberToOctave(pitch.number)
   #name = pitch.tools.pcToPitchNameFlats[pitch.pc]
   octave = pitchtools_pitch_number_to_octave(pitch.number)
   name = pitchtools_pc_to_pitch_name_flats(pitch.pc)
   pitch.octave = octave
   pitch.name = name
