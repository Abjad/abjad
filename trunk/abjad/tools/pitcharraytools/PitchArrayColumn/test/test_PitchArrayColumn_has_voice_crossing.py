from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArrayColumn_has_voice_crossing_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert not array.columns[0].has_voice_crossing
    assert array.columns[1].has_voice_crossing
    assert array.columns[2].has_voice_crossing
    assert not array.columns[3].has_voice_crossing
