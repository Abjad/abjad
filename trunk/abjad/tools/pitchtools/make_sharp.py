from abjad.tools import iterate


def make_sharp(expr):

   from abjad.pitch.pitch import Pitch
   if isinstance(expr, Pitch):
      _pitch_renotate_sharps(expr)
   else:
      from abjad.leaf.leaf import _Leaf
      for leaf in iterate.naive(expr, _Leaf):
         if hasattr(leaf, 'pitches'):
            for pitch in leaf.pitches:
               _pitch_renotate_sharps(pitch)


def _pitch_renotate_sharps(pitch):

   octave = pitch.tools.pitchNumberToOctave(pitch.number)
   name = pitch.tools.pcToPitchNameSharps[pitch.pc]
   pitch.octave = octave
   pitch.name = name

