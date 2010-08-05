from abjad.tools.containertools._replace_half_of_elements_in_container_with_rests import \
   _replace_half_of_elements_in_container_with_rests


def replace_smaller_right_half_of_elements_in_container_with_little_endian_rests(container):
   r'''.. versionadded:: 1.1.2

   For container `C` of even length `l` replace the last ``l/2`` elements
   of `C` with little-endian rests::

      abjad> staff = Staff(macros.scale(10))
      abjad> containertools.replace_smaller_right_half_of_elements_in_container_with_little_endian_rests(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
         g'8
         r8
         r2
      }

   For container `C` of odd length `l` replace the last ``ceil(l/2)`` elements
   of `C` with little-endian rests::

      abjad> staff = Staff(macros.scale(11))
      abjad> containertools.replace_smaller_right_half_of_elements_in_container_with_little_endian_rests(staff)
      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
         g'8
         a'8
         r8
         r2
      }
   '''

   return _replace_half_of_elements_in_container_with_rests(
      container, 'right', 'left', 'little-endian')
