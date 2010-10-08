from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier
from abjad.tools.spannertools import Spanner


def list_named_chromatic_pitches_in_expr(expr):
   '''Get tuple of zero or more Abjad :class:`~abjad.tools.pitchtools.NamedChromaticPitch.NamedChromaticPitch` 
   instances from almost any expression. ::

      abjad> t = tuplettools.FixedDurationTuplet((2, 8), macros.scale(3))
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(t)
      ((NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(e, 4))

   ::

      abjad> t = Staff(macros.scale(4))
      abjad> beam = spannertools.BeamSpanner(t[:])
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(beam)
      ((NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(e, 4), NamedChromaticPitch(f, 4))

   ::

      abjad> pitch = NamedChromaticPitch('df', 5)
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(pitch)
      (NamedChromaticPitch(df, 5),)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(note)
      (NamedChromaticPitch(df, 5),)

   ::

      abjad> chord = Chord([0, 2, 10], (1, 4))
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(chord)
      (NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(bf, 4))

   ::
      
      abjad> pitchtools.list_named_chromatic_pitches_in_expr('foo')
      ( )

   ::

      abjad> pitchtools.list_named_chromatic_pitches_in_expr(Rest((1, 4)))
      ( )

   Works with pitch sets. ::

      abjad> pitch_set = pitchtools.NamedChromaticPitchSet([0, 2, 4, 5])
      abjad> pitchtools.list_named_chromatic_pitches_in_expr(pitch_set)
      (NamedChromaticPitch(c, 4), NamedChromaticPitch(d, 4), NamedChromaticPitch(e, 4), NamedChromaticPitch(f, 4))

   Raises neither :exc:`MissingPitchError` nor :exc:`ExtraPitchError`.

   .. note:: The logic implemented here to iterate over the contents of
      spanners is unusual but useful.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.get_named_chromatic_pitch_from_pitch_carrieres( )`` to
      ``pitchtools.list_named_chromatic_pitches_in_expr( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.list_named_pitches_in_expr( )`` to
      ``pitchtools.list_named_chromatic_pitches_in_expr( )``.
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
