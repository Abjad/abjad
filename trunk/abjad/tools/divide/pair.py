from abjad.container.container import Container
from abjad.exceptions.exceptions import AssignabilityError
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tools import construct
from abjad.tools import listtools
from abjad.tuplet.fd.tuplet import FixedDurationTuplet
import math


def pair(l, (n, d), together = False):
   '''Divide duration pair (n, d) according to list l.
      Note that denominator d is interpreter as the basic tuplet unit.
      This explains why the function accepts a pair rather than a Rational.

      >>> divide.pair([1], (7, 16))
      (c'4..)

      >>> divide.pair([1, 2], (7, 16))
      (6:7, c'8, c'4)

      >>> divide.pair([1, 2, 4], (7, 16))
      (c'16, c'8, c'4)

      >>> divide.pair([1, 2, 4, 1], (7, 16))
      (8:7, c'16, c'8, c'4, c'16)

      >>> divide.pair([1, 2, 4, 1, 2], (7, 16))
      (10:7, c'16, c'8, c'4, c'16, c'8)

      >>> divide.pair([1, 2, 4, 1, 2, 4], (7, 16))
      (c'32, c'16, c'8, c'32, c'16, c'8)'''


   duration = (n, d)

   if len(l) == 0:
      raise ValueError('must divide list l of length > 0.')

   if len(l) == 1:
      if l[0] > 0:
         try:
            return Container([Note(0, duration)])
         except AssignabilityError:
            return Container(construct.notes(0, duration))
      elif l[0] < 0:
         try:
            return Container([Rest(duration)])
         except AssignabilityError:
            return Container(construct.rests(duration))
      else:
         raise ValueError('no divide zero values.')

   if len(l) > 1:
      exponent = int(math.log(listtools.weight(l), 2) - math.log(n, 2))
      denominator = int(d * 2 ** exponent)
      music = [ ]
      for x in l:
         if not x:
            raise ValueError('no divide zero values.')
         if x > 0:
            try:
               music.append(Note(0, (x, denominator)))
            except AssignabilityError:
               music.extend(construct.notes(0, (x, denominator)))
         else:
            music.append(Rest((-x, denominator)))
      return FixedDurationTuplet(duration, music)
