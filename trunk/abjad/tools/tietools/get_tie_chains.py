from abjad.exceptions import MissingSpannerError
from abjad.tools import check
from abjad.tools import iterate
from abjad.leaf.leaf import _Leaf


def get_tie_chains(components):
   '''This function returns all tie chains in components. A tie chain may 
   not encompass all the leaves spanned by its corresponding Tie spanner, 
   but only those found in the given list. i.e. the function returns the 
   intersection between all the leav es spanned by all tie spanners touching 
   the components given and the leaves found in the given components list.'''

   check.assert_components(components)

   ## collect tie spanners in components
   tie_spanners = [ ]
   for component in components:
      if component.tie.spanned:
         spanner = component.tie.spanner
         if not spanner in tie_spanners:
            tie_spanners.append(component.tie.spanner)

   ## get leaves to fuse  
   result = [ ]
   leaves_in_components = list(iterate.naive(components, _Leaf))
   for spanner in tie_spanners:
      leaves_intersecting = [ ]
      for leaf in spanner.leaves:
         if leaf in leaves_in_components:
            leaves_intersecting.append(leaf)
      result.append(tuple(leaves_intersecting))
   return result 
