from abjad.helpers.iterate import iterate
from abjad.helpers.leaf_duration_change import leaf_duration_change


def container_contents_scale(container, multiplier):
   '''Change all leaves in measure by multiplier.
      Return measure.

      TODO: merge leaf_duration_change and leaf_split_binary.
      TODO: generalize this helper to work on tuplets, too.'''

   for leaf in list(iterate(container, '_Leaf')):
      new_written_duration = multiplier * leaf.duration.written
      leaf_duration_change(leaf, new_written_duration) 
