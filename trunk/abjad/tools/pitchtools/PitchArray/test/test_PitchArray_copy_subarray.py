from abjad import *


def test_PitchArray_copy_subarray_01( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
   array[0].cells[0].pitches.append(0)
   array[0].cells[1].pitches.append(2)
   array[1].cells[2].pitches.append(4)

   '''
   [c'] [d'    ] [  ]
   [       ] [ ] [e']
   '''

   subarray = array.copy_subarray((0, 0), (2, 2))

   '''
   [c'] [d']
   [       ]
   '''

   assert subarray.dimensions == (2, 2)
   assert subarray.cell_widths_by_row == ((1, 1), (2,))
   assert subarray.pitches_by_row == ((Pitch(0), Pitch(2)), ())
