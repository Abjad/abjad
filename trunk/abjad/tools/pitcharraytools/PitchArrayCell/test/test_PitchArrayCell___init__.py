# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.pitcharraytools.PitchArrayCell.PitchArrayCell \
	import PitchArrayCell
import py.test


def test_PitchArrayCell___init___01():
    r'''Init empty.
    '''

    cell = PitchArrayCell()
    assert cell.pitches == []
    assert cell.width == 1


def test_PitchArrayCell___init___02():
    r'''Init with positive integer width.
    '''

    cell = PitchArrayCell(2)
    assert cell.pitches == []
    assert cell.width == 2


def test_PitchArrayCell___init___03():
    r'''Init with pitch instance.
    '''

    cell = PitchArrayCell(pitchtools.NamedChromaticPitch(0))
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0)]
    assert cell.width == 1


def test_PitchArrayCell___init___04():
    r'''Init with list of pitch tokens.
    '''

    cell = PitchArrayCell([0, 2, 4])
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]
    assert cell.width == 1


def test_PitchArrayCell___init___05():
    r'''Init with list of pitch instances.
    '''

    cell = PitchArrayCell([pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)])
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]
    assert cell.width == 1


def test_PitchArrayCell___init___06():
    r'''Init with list of pitch pairs.
    '''

    cell = PitchArrayCell([('c', 4), ('d', 4), ('e', 4)])
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]
    assert cell.width == 1


def test_PitchArrayCell___init___07():
    r'''Init with pitch token, width pair.
    '''

    cell = PitchArrayCell((0, 2))
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0)]
    assert cell.width == 2


def test_PitchArrayCell___init___08():
    r'''Init with pitch instance, width pair.
    '''

    cell = PitchArrayCell((pitchtools.NamedChromaticPitch(0), 2))
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0)]
    assert cell.width == 2


def test_PitchArrayCell___init___09():
    r'''Init with pitch token list, width pair.
    '''

    cell = PitchArrayCell(([0, 2, 4], 2))
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]
    assert cell.width == 2


def test_PitchArrayCell___init___10():
    r'''Init with pitch instance list, width pair.
    '''

    cell = PitchArrayCell(([pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)], 2))
    assert cell.pitches == [pitchtools.NamedChromaticPitch(0), pitchtools.NamedChromaticPitch(2), pitchtools.NamedChromaticPitch(4)]
    assert cell.width == 2
