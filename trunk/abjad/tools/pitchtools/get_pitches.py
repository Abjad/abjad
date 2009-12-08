from abjad.exceptions import ExtraPitchError
from abjad.exceptions import MissingPitchError
from abjad.spanners import Spanner
from abjad.tools import iterate
from abjad.tools.pitchtools.get_pitch import get_pitch as \
   get_pitch


def get_pitches(expr):
   '''Get tuple of zero or more Abjad :class:`~abjad.Pitch` 
   instances from almost any expression. ::

      abjad> t = FixedDurationTuplet((2, 8), construct.scale(3))
      abjad> pitchtools.get_pitches(t)
      ((Pitch(c, 4), Pitch(d, 4), Pitch(e, 4))

   ::

      abjad> t = Staff(construct.scale(4))
      abjad> beam = Beam(t[:])
      abjad> pitchtools.get_pitches(beam)
      ((Pitch(c, 4), Pitch(d, 4), Pitch(e, 4), Pitch(f, 4))

   ::

      abjad> pitch = Pitch('df', 5)
      abjad> pitchtools.get_pitches(pitch)
      (Pitch(df, 5),)

   ::

      abjad> note = Note(('df', 5), (1, 4))
      abjad> pitchtools.get_pitches(note)
      (Pitch(df, 5),)

   ::

      abjad> chord = Chord([0, 2, 10], (1, 4))
      abjad> pitchtools.get_pitches(chord)
      (Pitch(c, 4), Pitch(d, 4), Pitch(bf, 4))

   ::
      
      abjad> pitchtools.get_pitches('foo')
      ()

   ::

      abjad> pitchtools.get_pitches(Rest((1, 4)))
      ()

   Works with pitch sets. ::

      abjad> pitch_set = pitchtools.PitchSet([0, 2, 4, 5])
      abjad> pitchtools.get_pitches(pitch_set)
      (Pitch(c, 4), Pitch(d, 4), Pitch(e, 4), Pitch(f, 4))

   Raises neither :exc:`MissingPitchError` nor :exc:`ExtraPitchError`.

   .. note:: The logic implemented here to iterate over the contents of \
      spanners is unusual but useful.
   '''
   from abjad.tools.pitchtools.PitchSet import PitchSet

   try:
      result = get_pitch(expr)
      return (result, )
   except (TypeError, MissingPitchError, ExtraPitchError):
      result = [ ]
      if hasattr(expr, 'pitches'):
         result.extend(expr.pitches)
      elif isinstance(expr, Spanner):
         for leaf in expr.leaves:
            result.extend(leaf.pitches)
      elif isinstance(expr, PitchSet):
         pitches = list(expr)
         pitches.sort( )
         pitches = tuple(pitches)
         return pitches
      elif isinstance(expr, (list, tuple, set)):
         for x in expr:
            result.extend(get_pitches(x))
      else:
         for leaf in iterate.leaves_forward_in(expr):
            result.extend(leaf.pitches)
      return tuple(result)
