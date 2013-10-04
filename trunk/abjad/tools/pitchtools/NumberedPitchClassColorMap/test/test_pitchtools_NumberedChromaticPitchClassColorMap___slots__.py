# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_NumberedChromaticPitchClassColorMap___slots___01():
    r'''Numbered chromatic pitch-class color maps are immutable.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    numbered_pitch_class_color_map = pitchtools.NumberedPitchClassColorMap(
        pitches, colors)

    assert py.test.raises(AttributeError, "numbered_pitch_class_color_map.foo = 'bar'")
