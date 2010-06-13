from abjad.note import Note
from abjad.rational import Rational
from abjad.tools import durtools
from abjad.tools import mathtools


def notes_curve(pitches, total, start, stop, exp='cosine', 
   written=Rational(1, 8)):
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

      abjad> construct.notes_curve([1,2], (1, 2), (1, 4), (1, 8))
      [Note(cs', 8 * 113/64), Note(d', 8 * 169/128), Note(cs', 8 * 117/128)]
      abjad> x = Voice(_)
      abjad> x.duration.prolated
      Rational(1, 2)
   '''

   total = Rational(*durtools.token_unpack(total))
   start = Rational(*durtools.token_unpack(start))
   stop = Rational(*durtools.token_unpack(stop))
   written = Rational(*durtools.token_unpack(written))

   dts = mathtools.interpolate_divide(total, start, stop, exp)

   ## convert floats to rationals
   dts = [Rational(int(round(x * 2**10)), 2**10) for x in dts]

   ## make notes
   result = [ ]
   for i, dt in enumerate(dts):
      note = Note(pitches[i % len(pitches)], written)
      note.duration.multiplier = dt / written 
      result.append(note)
   return result
