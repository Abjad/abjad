from abjad.component import _Component


def get_dominant_between(left, right):
   '''Return Python list of (spanner, index) pairs.
   'left' must be either an Abjad component or None.
   'right' must be either an Abjad component or None.

   If both 'left' and 'right' are components,
   then 'left' and 'right' must be thread-contiguous.

   This is a special version of spannertools.get_dominant( ).
   This version is useful for finding spanners that dominant
   a zero-length 'crack' between components, as in t[2:2].
   '''
   from abjad.tools import componenttools
      
   if left is None or right is None:
      return set([ ])

   assert componenttools.all_are_thread_contiguous_components([left, right])

   dominant_spanners = left.spanners.contained & right.spanners.contained
   components_after_gap = right._navigator._contemporaneousStartComponents
   
   receipt = set([ ])
   for spanner in dominant_spanners:
      for component in components_after_gap:
         if component in spanner:
            index = spanner.index(component)
            receipt.add((spanner, index))
            continue   

   return receipt
