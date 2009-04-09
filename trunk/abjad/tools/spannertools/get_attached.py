from abjad.helpers.assert_components import assert_components


def get_attached(components):
   '''Return unordered set of all spanners attaching to any
      component in 'components' or attaching to any of the children
      of any of the components in 'components'.'''

   ## check input
   assert_components(components, contiguity = 'strict', share = 'thread')
   
   ## accumulate spanners
   spanners = set([ ])
   for component in components:
      for spanner in list(component.spanners.attached):
         spanners.update((spanner, ))
      
   ## return spanners
   return spanners
