from abjad.rational import Rational
from abjad.skip import Skip


def skips_with_multipliers(written_duration, multiplied_durations):
   '''.. versionadded:: 1.1.2

   Construct `written_duration` skips with `multiplied_durations`::
   
      abjad> construct.skips_with_multipliers(Rational(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)])
      [Skip(4 * 2), Skip(4 * 4/3), Skip(4 * 1), Skip(4 * 4/5)]

   Useful for making invisible layout voices.
   '''

   ## initialize skips and written duration
   skips = [ ]
   written_duration = Rational(written_duration)

   ## make skips
   for multiplied_duration in multiplied_durations:
      multiplied_duration = Rational(multiplied_duration)
      skip = Skip(written_duration)
      multiplier = multiplied_duration / written_duration
      skip.duration.multiplier = multiplier
      skips.append(skip)

   ## return skips
   return skips
