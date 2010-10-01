from abjad.components.Note import Note
from fractions import Fraction
from abjad.tools import durtools
from abjad.tools import mathtools


def make_accelerating_notes_with_lilypond_multipliers(pitches, total, start, stop, exp='cosine', 
   written=Fraction(1, 8)):
   '''Returns a train of notes with "continuously" changing effective 
   durations given as the written duration argument times the 
   computed interpolated multipliers. 
   The default written duration is 1/8 note. The durations are 
   interpolated from the `start` duration argument to the `stop` 
   duration argument. 
   The function returns as many interpolation values as necessary to 
   fill the `total` duration requested.
   The pitches of the notes are set cyclically from the `pitches` list.

   ::

      abjad> notetools.make_notes_curve([1,2], (1, 2), (1, 4), (1, 8))
      [Note(cs', 8 * 113/64), Note(d', 8 * 169/128), Note(cs', 8 * 117/128)]
      abjad> x = Voice(_)
      abjad> x.duration.prolated
      Fraction(1, 2)

   .. versionchanged:: 1.1.2
      renamed ``construct.notes_curve( )`` to
      ``notetools.make_accelerating_notes_with_lilypond_multipliers( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.make_accelerating_notes_with_lilypond_multipliers( )`` to
      ``notetools.make_accelerating_notes_with_lilypond_multipliers( )``.
   '''

   total = Fraction(*durtools.duration_token_to_reduced_duration_pair(total))
   start = Fraction(*durtools.duration_token_to_reduced_duration_pair(start))
   stop = Fraction(*durtools.duration_token_to_reduced_duration_pair(stop))
   written = Fraction(*durtools.duration_token_to_reduced_duration_pair(written))

   dts = mathtools.interpolate_divide(total, start, stop, exp)

   ## convert floats to rationals
   dts = [Fraction(int(round(x * 2**10)), 2**10) for x in dts]

   ## make notes
   result = [ ]
   for i, dt in enumerate(dts):
      note = Note(pitches[i % len(pitches)], written)
      note.duration.multiplier = dt / written 
      result.append(note)
   return result
