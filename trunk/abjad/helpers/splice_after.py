from abjad.component.component import _Component


def splice_after(component, new_components):
   '''Splice new_components after component;
      return list of [component] + new_components.'''

   assert isinstance(component, _Component)
   assert all([isinstance(x, _Component) for x in new_components])

   component.parentage._splice(new_components)
   component.spanners._splice(new_components)
   return [component] + new_components
