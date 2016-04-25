# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import NumberedPitchClassColorMap


def test_pitchtools_NumberedPitchClassColorMap___repr___01():
    r'''Numbered pitch-class color map repr is evaluable.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    numbered_pitch_class_color_map_1 = pitchtools.NumberedPitchClassColorMap(
        pitches, colors)
    numbered_pitch_class_color_map_2 = eval(repr(
        numbered_pitch_class_color_map_1))

    assert isinstance(numbered_pitch_class_color_map_1,
        pitchtools.NumberedPitchClassColorMap)
    assert isinstance(numbered_pitch_class_color_map_2,
        pitchtools.NumberedPitchClassColorMap)
