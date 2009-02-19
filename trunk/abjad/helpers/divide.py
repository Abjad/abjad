from abjad.container.container import Container
from abjad.helpers.chop import chop
from abjad.helpers.weight import weight
from abjad.note.note import Note
from abjad.rest.rest import Rest
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


def divide(l, (n, d), together = False):
   '''
   Divide duration (n, d) according to list l.
   Note that denominator d is interpreter as the basic tuplet unit;
   this explains why the function accepts a pair rather than a Rational.

   >>> divide([1], 7, 16)
   (c'4..)

   >>> divide([1, 2], 7, 16)
   (6:7, c'8, c'4)

   >>> divide([1, 2, 4], 7, 16)
   (c'16, c'8, c'4)

   >>> divide([1, 2, 4, 1], 7, 16)
   (8:7, c'16, c'8, c'4, c'16)

   >>> divide([1, 2, 4, 1, 2], 7, 16)
   (10:7, c'16, c'8, c'4, c'16, c'8)

   >>> divide([1, 2, 4, 1, 2, 4], 7, 16)
   (c'32, c'16, c'8, c'32, c'16, c'8)
   '''

   from abjad.exceptions.exceptions import AssignabilityError
   from abjad.tools import construct
   from math import log

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
      exponent = chop(log(weight(l), 2) - log(n, 2))
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
