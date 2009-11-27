from abjad.tools.pitchtools.PitchArray import PitchArray
import copy


def merge_pitch_arrays(pitch_arrays):
   '''.. versionadded:: 1.1.2

   Merge `pitch_arrays`. ::

      abjad> array_1 = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
      abjad> print array_1
      [ ] [     ] [ ]
      [     ] [ ] [ ]
   
   ::

      abjad> array_2 = pitchtools.PitchArray([[3, 4], [4, 3]])
      [     ] [         ]
      [         ] [     ]
   
   ::

      abjad> array_3 = pitchtools.PitchArray([[1, 1], [1, 1]])
      [ ] [ ]
      [ ] [ ]

   ::

      abjad> merged_array = pitchtools.merge_pitch_arrays([array_1, array_2, array_3])
      abjad> print merged_array
      [ ] [     ] [ ] [     ] [         ] [ ] [ ]
      [     ] [ ] [ ] [         ] [     ] [ ] [ ]
   '''

   if not all([isinstance(x, PitchArray) for x in pitch_arrays]):
      raise TypeError('must be pitch arrays.')

   if not pitch_arrays:
      return PitchArray( )

   merged_array = copy.copy(pitch_arrays[0])
   for pitch_array in pitch_arrays[1:]:
      merged_array += pitch_array

   return merged_array
