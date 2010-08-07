from abjad.tools.containertools._replace_first_n_elements_in_container_with_rests import \
   _replace_first_n_elements_in_container_with_rests


def replace_n_edge_elements_in_container_with_big_endian_rests(container, n):
   r'''.. versionadded:: 1.1.2

   For positive `n` replace first `n` elements in `container` with big-endian rests::

      abjad> staff = Staff(macros.scale(6))
      abjad> containertools.replace_n_edge_elements_in_container_with_big_endian_rests(staff, 5)
      abjad> f(staff)
      \new Staff {
         r2
         r8
         a'8
      }

   For negative `n` replace last `n` elements in `container` with big-endian rests::

      abjad> staff = Staff(macros.scale(6))
      abjad> containertools.replace_n_edge_elements_in_container_with_big_endian_rests(staff, -5)
      abjad> f(staff)
      \new Staff {
         c'8
         r2
         r8
      }

   .. versionchanged:: 1.1.2
      renamed ``containertools.replace_first_n_elements_in_container_with_big_endian_rests( )`` to
      ``containertools.replace_n_edge_elements_in_container_with_big_endian_rests( )``.
   '''

   if 0 <= n:
      rested_half = 'left'
   else:
      rested_half = 'right'

   return _replace_first_n_elements_in_container_with_rests(container, n, rested_half, 'big-endian')

   
