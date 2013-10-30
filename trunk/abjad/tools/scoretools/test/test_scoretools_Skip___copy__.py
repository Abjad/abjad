# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_scoretools_Skip___copy___01():
    r'''Copy skip.
    '''

    skip_1 = scoretools.Skip((1, 4))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, scoretools.Skip)
    assert isinstance(skip_2, scoretools.Skip)
    assert skip_1.lilypond_format == skip_2.lilypond_format
    assert skip_1 is not skip_2


def test_scoretools_Skip___copy___02():
    r'''Copy skip with LilyPond multiplier.
    '''

    skip_1 = scoretools.Skip((1, 4), (1, 2))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, scoretools.Skip)
    assert isinstance(skip_2, scoretools.Skip)
    assert skip_1.lilypond_format == skip_2.lilypond_format
    assert skip_1 is not skip_2


def test_scoretools_Skip___copy___03():
    r'''Copy skip with LilyPond grob overrides and LilyPond context settings.
    '''

    skip_1 = scoretools.Skip((1, 4))
    skip_1.override.staff.note_head.color = 'red'
    skip_1.override.accidental.color = 'red'
    skip_1.set.tuplet_full_length = True
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, scoretools.Skip)
    assert isinstance(skip_2, scoretools.Skip)
    assert skip_1.lilypond_format == skip_2.lilypond_format
    assert skip_1 is not skip_2
