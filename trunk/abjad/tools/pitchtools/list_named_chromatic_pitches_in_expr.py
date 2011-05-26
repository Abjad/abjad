from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.spannertools import Spanner


def list_named_chromatic_pitches_in_expr(expr):
   '''.. versionadded:: 1.1.2

   List named chromatic pitches in `expr`::

      abjad> t = Staff("c'4 d'4 e'4 f'4")
      abjad> beam = spannertools.BeamSpanner(t[:])
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(beam)
      ((NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(e, 4), NamedChromaticPitch(f, 4))
   '''
   from abjad.components import Rest
   from abjad.tools import leaftools
   from abjad.tools.pitchtools.NamedChromaticPitchSet import NamedChromaticPitchSet

   try:
      result = get_named_chromatic_pitch_from_pitch_carrier(expr)
      return (result, )
   except (TypeError, MissingPitchError, ExtraPitchError):
      result = [ ]
      if hasattr(expr, 'pitches'):
         result.extend(expr.pitches)
      elif isinstance(expr, Spanner):
         for leaf in expr.leaves:
            if hasattr(leaf, 'pitch') and not isinstance(leaf, Rest):
               result.append(leaf.pitch)
            elif hasattr(leaf, 'pitches'):
               result.extend(leaf.pitches)
      elif isinstance(expr, NamedChromaticPitchSet):
         pitches = list(expr)
         pitches.sort( )
         pitches = tuple(pitches)
         return pitches
      elif isinstance(expr, (list, tuple, set)):
         for x in expr:
            result.extend(list_named_chromatic_pitches_in_expr(x))
      else:
         for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            if hasattr(leaf, 'pitch') and not isinstance(leaf, Rest):
               result.append(leaf.pitch)
            elif hasattr(leaf, 'pitches'):
               result.extend(leaf.pitches)
      return tuple(result)
