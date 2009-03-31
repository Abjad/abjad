from abjad.rational.rational import Rational
from abjad.tools import construct


def container_rest_by_count(container, i, rested_half, direction = 'automatic'):
   '''Glom element on rested_half of index i in container.
      Transform glommed duration into rests.
      Return container.'''

   ## assert keyword values
   assert rested_half in ('left', 'right')
   assert direction in ('automatic', 'big-endian', 'little-endian')

   ## set rest chain direction based on rested part of container
   if direction == 'automatic':
      if rested_half == 'left':
         direction = 'little-endian'
      elif rested_half == 'right':
         direction = 'big-endian'

   ## get elements to replace in container
   if rested_half == 'left':
      elements_to_replace = container[:i]
   elif rested_half == 'right':
      elements_to_replace = container[i:]

   ## if there are elements to replace
   if elements_to_replace:

      ## find preprolated duration of elements to replace
      duration = sum([x.duration.preprolated for x in elements_to_replace])

      ## construct rest chain equal in preprolated duration to replace
      rests = construct.rests(duration, direction)

      ## replace elements in rested_half of container with rest chain
      if rested_half == 'left':
         container[:i] = rests
      else:
         container[i:] = rests

   ## return container
   return container
