from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.tools.spannertools import Spanner
from abjad.tools.pitchtools.get_named_pitch_from_pitch_carrier import get_named_pitch_from_pitch_carrier


def list_named_pitches_in_expr(expr):
   '''Get tuple of zero or more Abjad :class:`~abjad.tools.pitchtools.NamedPitch.NamedPitch` 
   instances from almost any expression. ::

      abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> pitchtools.list_named_pitches_in_expr(t)
      ((NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(e, 4))

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(t[:])
      abjad> pitchtools.list_named_pitches_in_expr(beam)
      ((NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(e, 4), NamedPitch(f, 4))

   ::

      abjad> pitch = NamedPitch('df', 5)
      abjad> pitchtools.list_named_pitches_in_expr(pitch)
      (NamedPitch(df, 5),)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> pitchtools.list_named_pitches_in_expr(note)
      (NamedPitch(df, 5),)

   ::

      abjad> chord = Chord([0, 2, 10], (1, 4))
      abjad> pitchtools.list_named_pitches_in_expr(chord)
      (NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(bf, 4))

   ::
      
      abjad> pitchtools.list_named_pitches_in_expr('foo')
      ()

   ::

      abjad> pitchtools.list_named_pitches_in_expr(Rest((1, 4)))
      ()

   Works with pitch sets. ::

      abjad> pitch_set = pitchtools.NamedPitchSet([0, 2, 4, 5])
      abjad> pitchtools.list_named_pitches_in_expr(pitch_set)
      (NamedPitch(c, 4), NamedPitch(d, 4), NamedPitch(e, 4), NamedPitch(f, 4))

   Raises neither :exc:`MissingPitchError` nor :exc:`ExtraPitchError`.

   .. note:: The logic implemented here to iterate over the contents of
      spanners is unusual but useful.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_named_pitch_from_pitch_carrieres( )`` to
      ``pitchtools.list_named_pitches_in_expr( )``.
   '''
   from abjad.tools import leaftools
   from abjad.tools.pitchtools.NamedPitchSet import NamedPitchSet

   try:
      result = get_named_pitch_from_pitch_carrier(expr)
      return (result, )
   except (TypeError, MissingPitchError, ExtraPitchError):
      result = [ ]
      if hasattr(expr, 'pitches'):
         result.extend(expr.pitches)
      elif isinstance(expr, Spanner):
         for leaf in expr.leaves:
            result.extend(leaf.pitches)
      elif isinstance(expr, NamedPitchSet):
         pitches = list(expr)
         pitches.sort( )
         pitches = tuple(pitches)
         return pitches
      elif isinstance(expr, (list, tuple, set)):
         for x in expr:
            result.extend(list_named_pitches_in_expr(x))
      else:
         for leaf in leaftools.iterate_leaves_forward_in_expr(expr):
            result.extend(leaf.pitches)
      return tuple(result)
