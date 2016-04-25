# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayColumn_start_cells_01():

    array = pitchtools.PitchArray([
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
