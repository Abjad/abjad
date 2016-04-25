# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchArrayRow_append_01():
    r'''Append cell by positive integer width.
    '''

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(NamedPitch(0))
    array[0].cells[1].append_pitch(NamedPitch(2))
    array[0].cells[1].append_pitch(NamedPitch(4))

    '''
    [c'] [d' e'    ] [ ]
    [          ] [ ] [ ]
    '''

    cell = pitchtools.PitchArrayCell(width=1)
    array[0].append(cell)
    cell = pitchtools.PitchArrayCell(width=1)
    array[1].append(cell)

    '''
    [c'] [d' e'    ] [ ] [ ]
    [          ] [ ] [ ] [ ]
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [ ]\n[          ] [ ] [ ] [ ]"


def test_pitchtools_PitchArrayRow_append_02():

    array = pitchtools.PitchArray([[1, 2, 1], [2, 1, 1]])
    array[0].cells[0].append_pitch(NamedPitch(0))
    array[0].cells[1].append_pitch(NamedPitch(2))
    array[0].cells[1].append_pitch(NamedPitch(4))

    '''
    [c'] [d' e'     ] [ ]
    [           ] [ ] [ ]
    '''

    cell = pitchtools.PitchArrayCell(pitches=[0])
    array[0].append(cell)
    cell = pitchtools.PitchArrayCell(pitches=[2])
    array[1].append(cell)

    '''
    [c'] [d' e'    ] [ ] [c']
    [          ] [ ] [ ] [d']
    '''

    assert str(array) == "[c'] [d' e'    ] [ ] [c']\n[          ] [ ] [ ] [d']"
