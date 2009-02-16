from abjad.rational.rational import Rational
from abjad.tools import construct


## TODO: Write container_glom_by_count(container)

def measure_rest_by_count(measure, i, rested_half, direction = 'automatic'):
   '''Create glom element on rest side of index i in measure.
      Transform glommed duration into rests.

      Return measure.

      TODO: figure out how to handle spanners.
      TODO: generalize measure to any (sequential) container.'''

   # assert keyword values
   assert rested_half in ('left', 'right')
   assert direction in ('automatic', 'big-endian', 'little-endian')

   # set rest chain direction based on rested part of measure
   if direction == 'automatic':
      if rested_half == 'left':
         direction = 'little-endian'
      elif rested_half == 'right':
         direction = 'big-endian'

   # get elements to replace in measure
   if rested_half == 'left':
      elements_to_replace = measure[:i]
   elif rested_half == 'right':
      elements_to_replace = measure[i:]

   # if there are elements to replace
   if elements_to_replace:

      # find preprolated duration of elements to replace
      duration = Rational(0)
      for element in elements_to_replace:
         duration += element.duration.preprolated

      # construct rest chain equal in preprolated duration to replace
      rests = construct.rests(duration, direction)

      # replace elements in rested_half of measure with rest chain
      if rested_half == 'left':
         measure[:i] = rests
      else:
         measure[i:] = rests

   # return measure
   return measure
