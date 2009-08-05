from abjad.tools.leaftools.duration_change import duration_change


def duration_scale(leaf, multiplier):
   '''Scale leaf duration by multiplier.
      Wraps leaftools.duration_change.
      Returns leaf.'''

   # find new leaf written duration
   new_written_duration = multiplier * leaf.duration.written

   # assign new leaf written duration and return structure
   return duration_change(leaf, new_written_duration)
