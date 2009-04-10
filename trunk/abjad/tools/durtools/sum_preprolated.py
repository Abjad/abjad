#from abjad.helpers.assert_components import assert_components


## TODO: Maybe move durtools.sum_preprolated to component-centered module? ##

def sum_preprolated(components):
   '''Components must be strictly contiguous and in same parent.

      Return sum of preprolated duration of all components in list.'''

   from abjad.helpers.assert_components import assert_components

   ## check input
   assert_components(components, contiguity = 'strict', share = 'parent')

   ## sum preprolated durations
   result = sum([component.duration.preprolated for component in components])

   ## return sum
   return result
