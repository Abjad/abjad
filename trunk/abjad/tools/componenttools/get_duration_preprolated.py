from abjad.tools import check


def get_duration_preprolated(components):
   '''Components must be strictly contiguous and in same parent.

      Return sum of preprolated duration of all components in list.'''

   ## check input
   check.assert_components(components, contiguity = 'strict', share = 'parent')

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
