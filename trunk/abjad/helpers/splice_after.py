from abjad.component.component import _Component


def splice_after(component, new_components):
   '''Splice new_components after component;
      return list of [component] + new_components.'''

   assert isinstance(component, _Component)
   assert all([isinstance(x, _Component) for x in new_components])

   # if component has parent
   if component._parent is not None:

      # find index of component in parent
      parent_index = component._parent.index(component)

      # find slice insertion index
      index = parent_index + 1

      # insert new components in parent after component
      component._parent[index:index] = new_components

   # for every spanner attached to component
   for spanner in list(component.spanners.attached):

      # find index of component in spanner
      spanner_index = spanner.index(component)

      # find slice insertion index
      index = spanner_index + 1

      # insert new leaves in spanner after component
      spanner[index:index] = new_components

   # return component followed by new_components
   return [component] + new_components
