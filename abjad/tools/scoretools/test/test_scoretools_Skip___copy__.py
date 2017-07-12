# -*- coding: utf-8 -*-
import abjad
import copy


def test_scoretools_Skip___copy___01():
    r'''Copy skip.
    '''

    skip_1 = abjad.Skip((1, 4))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert format(skip_1) == format(skip_2)
    assert skip_1 is not skip_2


def test_scoretools_Skip___copy___02():
    r'''Copy skip with LilyPond multiplier.
    '''

    skip_1 = abjad.Skip('s4')
    abjad.attach(abjad.Multiplier(1, 2), skip_1)
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert format(skip_1) == format(skip_2)
    assert skip_1 is not skip_2


def test_scoretools_Skip___copy___03():
    r'''Copy skip with LilyPond grob abjad.overrides and LilyPond context abjad.settings.
    '''

    skip_1 = abjad.Skip((1, 4))
    abjad.override(skip_1).staff.note_head.color = 'red'
    abjad.override(skip_1).accidental.color = 'red'
    abjad.setting(skip_1).tuplet_full_length = True
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert format(skip_1) == format(skip_2)
    assert skip_1 is not skip_2
