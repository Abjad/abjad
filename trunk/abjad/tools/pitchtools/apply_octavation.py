from abjad.octavation import Octavation
from abjad.tools.pitchtools.get_pitches import get_pitches


def apply_octavation(expr, 
   ottava_altitude = None, quindecisima_altitude = None):
   r""".. versionadded:: 1.1.1

   Apply :class:`~abjad.octavation.spanner.Octavation` to `expr`
   dependent on the :term:`altitude` of the maximum pitch in `expr`. ::

      abjad> t = RigidMeasure((4, 8), construct.notes([24, 26, 27, 29], [(1, 8)]))
      abjad> pitchtools.apply_octavation(t, ottava_altitude = 14)
      Octavation(|4/8, c'''8, d'''8, ef'''8, f'''8|)

   ::

      abjad> print t.format
         \time 4/8
         \ottava #1
         c'''8
         d'''8
         ef'''8
         f'''8
         \ottava #0
   """

   pitches = get_pitches(expr)
   max_pitch = max(pitches)
   max_altitude = max_pitch.altitude

   if ottava_altitude is not None:
      if ottava_altitude <= max_altitude:
         octavation = Octavation(expr)   
         octavation.start = 1
         if quindecisima_altitude is not None:
            if quindecisima_altitude <= max_altitude:
               octavation.start = 2
         #else:
         #   octavation.start = 1

   try:
      return octavation
   except NameError:
      return None
