# -*- coding: utf-8 -*-
import pytest
from abjad import *
import pytest


def test_pitchtools_NumberedPitchClassColorMap_01():
    r'''Test basic pc color map attributes.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    pcm = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    "PitchClassColorMap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])"

    assert pcm.colors == ['red', 'green', 'blue']
    assert pcm.pairs == [
        (0, 'green'),
        (1, 'blue'),
        (2, 'red'),
        (3, 'blue'),
        (4, 'red'),
        (5, 'green'),
        (6, 'blue'),
        (7, 'blue'),
        (8, 'green'),
        (9, 'red'),
        (10, 'red'),
        (11, 'green'),
        ]
    assert pcm.pitch_iterables == [
        [-8, 2, 10, 21],
        [0, 11, 32, 41],
        [15, 25, 42, 43],
        ]
    assert pcm.is_twelve_tone_complete
    assert not pcm.is_twenty_four_tone_complete


def test_pitchtools_NumberedPitchClassColorMap_02():
    r'''Test pc color map get item variations.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    pcm = pitchtools.NumberedPitchClassColorMap(pitches, colors)

    "PitchClassColorMap([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])"

    assert pcm[1] == 'blue'
    assert pcm[pitchtools.NumberedPitchClass(1)] == 'blue'
    assert pcm[pitchtools.NamedPitch(1)] == 'blue'

    assert pcm[13] == 'blue'
    assert pcm[pitchtools.NumberedPitchClass(13)] == 'blue'
    assert pcm[pitchtools.NamedPitch(13)] == 'blue'

    assert pytest.raises(Exception, "pcm['foo']")

    assert pcm.get(1) == 'blue'
    assert pcm.get('foo') is None
    assert pcm.get('foo', 'blah') == 'blah'
