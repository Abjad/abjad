from abjad.helpers.iterate import iterate
from abjad.helpers.leaf_duration_scale import leaf_duration_scale
from abjad.leaf.leaf import _Leaf


def container_contents_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.

      TODO: generalize this helper to work on tuplets, too.'''

   for component in container[:]:
      if isinstance(component, _Leaf):
         leaf_duration_scale(component, multiplier)
      else:
         pass
