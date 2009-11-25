from abjad.tools import listtools
from abjad.tools.pitchtools.PitchArray import PitchArray


def leaf_array_to_pitch_array_empty(leaf_array):
   '''.. versionadded:: 1.1.2

   Return empty pitch array corresponding to list-of-leaf-lists 
   `leaf_array`. ::

      abjad>
   '''

   from abjad.tools import leaftools

   offsets = leaftools.composite_offset_series(leaf_array)

   array_width = len(offsets) - 1
   array_depth = len(leaf_array)

   array = PitchArray(array_depth, array_width)

   for leaf_list in leaf_array:
      leaf_list_durations = [ ]
      pass

   return array
