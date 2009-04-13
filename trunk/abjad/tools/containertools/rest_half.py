from abjad.tools import mathtools
from abjad.tools.containertools.rest_by_count import rest_by_count


def rest_half(container, rested_half, bigger_half, 
   rest_direction = 'automatic'):
   '''Turn half of the elements in container into rests.
      Function works by the *number of* elements in container,
      and not, for example, by the *duration of* elements in container.

      Either the leftmost, or rightmost, elements in container may rest;
      set the 'rested_half' keyword to 'left' or 'right', respectively.

      Measures with 3, 5, 7 or some other odd number of elements
      read the mandatory 'bigger_half' parameter to decide whether 
      more elements on the left, or right, will group together into a half;
      set the bigger_half keyword to 'left', or 'right', respectively.

      The optional rest_direction keyword should be set to
      'automatic', 'big-endian' or 'little-endian'.
      The helper reads rest_direction only when the duration of
      new rests to construct is nonassignable, like 5/16 or 9/16.
      
      Return container.'''

   ## assert input types
   assert rested_half in ('left', 'right')
   assert bigger_half in ('left', 'right')
   assert rest_direction in ('automatic', 'big-endian', 'little-endian')

   ## do nothing to empty containers or containers of length 1
   container_length = len(container)
   if container_length in (0, 1):
      return container

   ## determine split index
   halves = mathtools.integer_halve(len(container), bigger = bigger_half)
   i = halves[0]

   ## rest container in place at split index
   rest_by_count(
      container, i, rested_half, direction = rest_direction)

   ## return rested container
   return container
