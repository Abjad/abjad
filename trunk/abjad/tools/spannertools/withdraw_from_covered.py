from abjad.tools.spannertools.get_covered import get_covered


def withdraw_from_covered(components):
   '''Find every spanner covered by 'components'.
      Withdraw all components in 'components' from covered spanners.
      Return 'components'.
      The operation always leaves all score trees in tact.
   '''
   from abjad.tools import componenttools

   ## check components
   assert componenttools.all_are_thread_contiguous_components(components)

   ## withdraw from covered spanners
   for spanner in get_covered(components):
      spanner.clear( )

   ## return components
   return components
