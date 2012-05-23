from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayColumn_start_cells_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), ([-2, -1.5], 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bf bqf     ]
    [g'      ] [fs'    ] []
    '''

    array.columns[0].start_cells == (array[0].cells[0], array[1].cells[0])
    array.columns[1].start_cells == (array[0].cells[1], )
    array.columns[2].start_cells == (array[0].cells[2], array[1].cells[1])
    array.columns[3].start_cells == ()
