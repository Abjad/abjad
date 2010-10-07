from abjad import *
from abjad.tools.pitchtools.PitchArray.PitchArrayCell.PitchArrayCell \
    import PitchArrayCell
import py.test


def test_PitchArrayCell_next_01( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

   '''
   [ ] [     ] [ ]
   [     ] [ ] [ ]
   '''

   assert array[0][1].next is array[0][3]


def test_PitchArrayCell_next_02( ):

   array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])

   '''
   [ ] [     ] [ ]
   [     ] [ ] [ ]
   '''

   assert py.test.raises(IndexError, 'array[0][-1].next')


def test_PitchArrayCell_next_03( ):

   cell = PitchArrayCell([pitchtools.NamedPitch(1)])

   assert py.test.raises(IndexError, 'cell.next')
