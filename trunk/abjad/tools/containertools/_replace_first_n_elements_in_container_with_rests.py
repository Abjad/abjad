from abjad.core import Rational
from abjad.tools import leaftools


def _replace_first_n_elements_in_container_with_rests(container, i, rested_half, 
   direction = 'automatic'):
   r'''Replace the `i` elements in the `rested_half` of `container` 
   with rests::

      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 5, 'left', 'automatic')
      abjad> f(staff)
      \new Staff {
         r8
         r2
         a'8
         b'8
      }
      
   ::
      
      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 5, 'left', 'big-endian')
      abjad> f(staff)
      \new Staff {
         r2
         r8
         a'8
         b'8
      }
      
   ::
      
      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 5, 'left', 'little-endian')
      abjad> f(staff)
      \new Staff {
         r8
         r2
         a'8
         b'8
      }
      
   ::
      
      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 2, 'right', 'automatic')
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         r2
         r8
      }
      
   ::
      
      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 2, 'right', 'big-endian')
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         r2
         r8
      }
      
   ::
      
      abjad> staff = Staff(macros.scale(7))
      abjad> containertools.rest_by_count(staff, 2, 'right', 'little-endian')
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         r8
         r2
      }

   Return `container`.

   Set `direction` to control the order of rests created.

   .. todo: replace 'left' and 'right' with positive and negative
      values of `i`.
   '''

   ## assert keyword values
   assert rested_half in ('left', 'right')

   if direction not in ('automatic', 'big-endian', 'little-endian'):
      raise ValueError('unknown direction: %s' % direction)

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
      rests = leaftools.make_rests(duration, direction)

      ## replace elements in rested_half of container with rest chain
      if rested_half == 'left':
         container[:i] = rests
      else:
         container[i:] = rests

   ## return container
   return container
