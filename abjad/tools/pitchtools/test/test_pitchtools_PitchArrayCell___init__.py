# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_PitchArrayCell___init___01():
    r'''Initializeempty.
    '''

    cell = pitchtools.PitchArrayCell()
    assert cell.pitches == []
    assert cell.width == 1


def test_pitchtools_PitchArrayCell___init___02():
    r'''Initialize with positive integer width.
    '''

    cell = pitchtools.PitchArrayCell(2)
    assert cell.pitches == []
    assert cell.width == 2


def test_pitchtools_PitchArrayCell___init___03():
    r'''Initialize with pitch instance.
    '''

    cell = pitchtools.PitchArrayCell(NamedPitch(0))
    assert cell.pitches == [NamedPitch(0)]
    assert cell.width == 1


def test_pitchtools_PitchArrayCell___init___04():
    r'''Initialize with list of pitch items.
    '''

    cell = pitchtools.PitchArrayCell([0, 2, 4])
    assert cell.pitches == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]
    assert cell.width == 1


def test_pitchtools_PitchArrayCell___init___05():
    r'''Initialize with list of pitch instances.
    '''

    cell = pitchtools.PitchArrayCell([NamedPitch(0), NamedPitch(2), NamedPitch(4)])
    assert cell.pitches == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]
    assert cell.width == 1


def test_pitchtools_PitchArrayCell___init___06():
    r'''Initialize with list of pitch pairs.
    '''

    cell = pitchtools.PitchArrayCell([('c', 4), ('d', 4), ('e', 4)])
    assert cell.pitches == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]
    assert cell.width == 1


def test_pitchtools_PitchArrayCell___init___07():
    r'''Initialize with pitch item, width pair.
    '''

    cell = pitchtools.PitchArrayCell((0, 2))
    assert cell.pitches == [NamedPitch(0)]
    assert cell.width == 2


def test_pitchtools_PitchArrayCell___init___08():
    r'''Initialize with pitch instance, width pair.
    '''

    cell = pitchtools.PitchArrayCell((NamedPitch(0), 2))
    assert cell.pitches == [NamedPitch(0)]
    assert cell.width == 2


def test_pitchtools_PitchArrayCell___init___09():
    r'''Initialize with pitch item list, width pair.
    '''

    cell = pitchtools.PitchArrayCell(([0, 2, 4], 2))
    assert cell.pitches == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]
    assert cell.width == 2


def test_pitchtools_PitchArrayCell___init___10():
    r'''Initialize with pitch instance list, width pair.
    '''

    cell = pitchtools.PitchArrayCell(([NamedPitch(0), NamedPitch(2), NamedPitch(4)], 2))
    assert cell.pitches == [NamedPitch(0), NamedPitch(2), NamedPitch(4)]
    assert cell.width == 2