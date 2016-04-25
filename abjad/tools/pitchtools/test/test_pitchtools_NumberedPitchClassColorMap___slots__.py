# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitchClassColorMap___slots___01():
    r'''Numbered pitch-class color maps are immutable.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    numbered_pitch_class_color_map = \
        pitchtools.NumberedPitchClassColorMap(pitches, colors)

    statement = "numbered_pitch_class_color_map.foo = 'bar'"
    assert pytest.raises(Exception, statement)
