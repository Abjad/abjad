# -*- encoding: utf-8 -*-
from abjad import *


def test_pitcharraytools_PitchArrayRow_append_01():
    r'''Append cell by positive integer width.
    '''

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(NamedPitch(0))
    array[0].cells[1].pitches.extend([NamedPitch(2), NamedPitch(4)])

    '''
    [c'] [d' e'    ] [ ]
    [          ] [ ] [ ]
    '''

    array[0].append(1)
    array[1].append(1)

    '''
    [c'] [d' e'    ] [ ] [ ]
    [          ] [ ] [ ] [ ]
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [ ]\n[          ] [ ] [ ] [ ]"


def test_pitcharraytools_PitchArrayRow_append_02():

    array = pitcharraytools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].pitches.append(NamedPitch(0))
    array[0].cells[1].pitches.extend([NamedPitch(2), NamedPitch(4)])

    '''
    [c'] [d' e'     ] [ ]
    [           ] [ ] [ ]
    '''

    array[0].append(NamedPitch(0))
    array[1].append(NamedPitch(2))

    '''
    [c'] [d' e'    ] [ ] [c']
    [          ] [ ] [ ] [d']
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [c']\n[          ] [ ] [ ] [d']"
