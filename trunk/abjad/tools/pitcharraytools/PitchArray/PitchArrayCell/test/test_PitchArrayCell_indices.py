from abjad import *
from abjad.tools.pitcharraytools.PitchArray.PitchArrayCell.PitchArrayCell \
   import PitchArrayCell
import py.test


def test_PitchArrayCell_indices_01( ):

   array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])

   '''
   [ ] [     ] [ ]
   [     ] [ ] [ ]
   '''

   assert array[0].cells[0].indices == (0, (0,))
   assert array[0].cells[1].indices == (0, (1, 2))
   assert array[0].cells[2].indices == (0, (3,))

   assert array[1].cells[0].indices == (1, (0, 1))
   assert array[1].cells[1].indices == (1, (2,))
   assert array[1].cells[2].indices == (1, (3,))


def test_PitchArrayCell_indices_02( ):

   cell = PitchArrayCell([pitchtools.NamedPitch(1)])

   assert py.test.raises(IndexError, 'cell.indices')
