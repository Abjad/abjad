from abjad.components import Note
from abjad.tools import durtools
from abjad.tools import mathtools
from fractions import Fraction


def make_accelerating_notes_with_lilypond_multipliers(pitches, total, start, stop, exp='cosine', 
   written = Fraction(1, 8)):
   '''Make accelerating notes with LilyPond multipliers::

      abjad> notetools.make_accelerating_notes_with_lilypond_multipliers([1,2], (1, 2), (1, 4), (1, 8))
      [Note(cs', 8 * 113/64), Note(d', 8 * 169/128), Note(cs', 8 * 117/128)]

   ::

      abjad> voice = Voice(_)
      abjad> voice.duration.prolated
      Fraction(1, 2)

   Set note pitches cyclically from `pitches`.

   Return as many interpolation values as necessary to fill the `total` duration requested.

   Interpolate durations from `start` to `stop`.

   Set note durations to `written` duration times computed interpolated multipliers. 

   Return list of notes.

   .. versionchanged:: 1.1.2
      renamed ``construct.notes_curve( )`` to
      ``notetools.make_accelerating_notes_with_lilypond_multipliers( )``.
   '''

   total = Fraction(*durtools.duration_token_to_duration_pair(total))
   start = Fraction(*durtools.duration_token_to_duration_pair(start))
   stop = Fraction(*durtools.duration_token_to_duration_pair(stop))
   written = Fraction(*durtools.duration_token_to_duration_pair(written))

   dts = mathtools.interpolate_divide(total, start, stop, exp)

   ## change floats to rationals
   dts = [Fraction(int(round(x * 2**10)), 2**10) for x in dts]

   ## make notes
   result = [ ]
   for i, dt in enumerate(dts):
      note = Note(pitches[i % len(pitches)], written)
      note.duration.multiplier = dt / written 
      result.append(note)
   return result
