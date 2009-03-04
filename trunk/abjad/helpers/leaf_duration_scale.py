from abjad.helpers.leaf_duration_change import leaf_duration_change


def leaf_duration_scale(leaf, multiplier):
   '''Scale leaf duration by multiplier.
      Wraps leaf_duration_change.
      Returns leaf.'''

   # find new leaf written duration
   new_written_duration = multiplier * leaf.duration.written

   # assign new leaf written duration and return structure
   return leaf_duration_change(leaf, new_written_duration)
