from abjad.rational.rational import Rational
from abjad.tools import construct


def measure_rest_by_count(measure, i, 
   rest = 'left', direction = 'little-endian'):
   '''Create glom element on rest side of index i in measure;
      transform glommed duration into rests;

      TODO: figure out how to handle spanners.
      TODO: generalize measure to any (sequential) container.'''

   if rest == 'left':
      elements_to_replace = measure[:i]
   elif rest == 'right':
      elements_to_replace = measure[i:]
   else:
      raise ValueError('must be left or right.')

   if elements_to_replace:
      duration = Rational(0)
      for element in elements_to_replace:
         duration += element.duration.preprolated
      rests = construct.rests(duration, direction)
      if rest == 'left':
         measure[:i] = rests
      else:
         measure[i:] = rests

   return rests
