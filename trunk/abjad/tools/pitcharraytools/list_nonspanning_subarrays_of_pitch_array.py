from abjad.tools import listtools
from abjad.tools.pitchtools.PitchArray import PitchArray


def list_nonspanning_subarrays_of_pitch_array(array):
   r'''.. versionadded:: 1.1.2

   Yield left-to-right nonspanning subarrays in `array`. ::

      abjad> array = pitchtools.PitchArray([
      ...     [2, 2, 3, 1],
      ...     [1, 2, 1, 1, 2, 1],
      ...     [1, 1, 1, 1, 1, 1, 1, 1]])
      abjad> print array
      [     ] [     ] [         ] [ ]
      [ ] [     ] [ ] [ ] [     ] [ ]
      [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

   ::

      abjad> subarrays = pitchtools.list_nonspanning_subarrays_of_pitch_array(array)
      abjad> len(subarrays)
      3

   ::

      abjad> print subarrays[0]
      [     ] [     ]
      [ ] [     ] [ ]
      [ ] [ ] [ ] [ ]

   ::

      abjad> print subarrays[1]
      [         ]
      [ ] [     ]
      [ ] [ ] [ ]

   ::

      abjad> print subarrays[2]
      [ ]
      [ ]
      [ ]

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.array_to_nonspanning_subarrays( )`` to
      ``pitchtools.list_nonspanning_subarrays_of_pitch_array( )``.
   '''

   if not isinstance(array, PitchArray):
      raise TypeError('must be pitch array.')
   
   unspanned_indices = [ ]
   for i in range(array.width + 1):
      if not array.has_spanning_cell_over_index(i):
         unspanned_indices.append(i)

   array_depth = array.depth
   subarrays = [ ]
   for start_column, stop_column in listtools.pairwise(unspanned_indices):
      upper_left_pair = (0, start_column)
      lower_right_pair = (array_depth, stop_column)
      subarray = array.copy_subarray(upper_left_pair, lower_right_pair)
      subarrays.append(subarray)
      
   return subarrays
