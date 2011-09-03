from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayRow_has_spanning_cell_over_index_01():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(0)
    array[0].cells[1].pitches.append(2)
    array[1].cells[2].pitches.append(4)

    '''
    [c'] [d'     ] [  ]
    [         ] [] [e']
    '''

    assert not array[0].has_spanning_cell_over_index(0)
    assert not array[0].has_spanning_cell_over_index(1)
    assert array[0].has_spanning_cell_over_index(2)
    assert not array[0].has_spanning_cell_over_index(3)
    assert not array[0].has_spanning_cell_over_index(99)

    assert not array[1].has_spanning_cell_over_index(0)
    assert array[1].has_spanning_cell_over_index(1)
    assert not array[1].has_spanning_cell_over_index(2)
    assert not array[1].has_spanning_cell_over_index(3)
    assert not array[1].has_spanning_cell_over_index(99)
