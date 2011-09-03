from abjad import *
from abjad.tools import pitcharraytools


def test_PitchArray_has_voice_crossing_01():

    array = pitcharraytools.PitchArray([
        [1, (2, 1), (-1.5, 2)],
        [(7, 2), (6, 1), 1],
        ])

    '''
    [  ] [d'] [bqf     ]
    [g'      ] [fs'] []
    '''

    assert array.has_voice_crossing
