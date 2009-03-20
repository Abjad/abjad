from abjad.component.component import _Component


def _get_subtree_dominant_spanners(component):
   '''Return list of all spanners attached to component or
      attached to any of the children of component with
      begin time less than or equal to begin time of component and
      end time greater than or equal to end time of component.

      That is, spanners that *temporally cover* component.'''

   if not isinstance(component, _Component):
      raise TypeError('Must be Abjad component.')

   subtree_begin = component.offset.score
   subtree_end = component.offset.score + component.duration.prolated

   dominant_spanners = [ ]
   for spanner in component.spanners.contained:
      if spanner.begin <= subtree_begin:
         if subtree_end <= spanner.end:
            dominant_spanners.append(spanner)

   return dominant_spanners
