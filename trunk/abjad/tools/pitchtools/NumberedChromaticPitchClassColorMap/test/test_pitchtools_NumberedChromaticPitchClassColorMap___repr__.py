from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitchClassColorMap


def test_pitchtools_NumberedChromaticPitchClassColorMap___repr___01():
    '''Numbered chromatic pitch-class color map repr is evaluable.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    numbered_chromatic_pitch_class_color_map_1 = pitchtools.NumberedChromaticPitchClassColorMap(
        pitches, colors)
    numbered_chromatic_pitch_class_color_map_2 = eval(repr(
        numbered_chromatic_pitch_class_color_map_1))

    assert isinstance(numbered_chromatic_pitch_class_color_map_1,
        pitchtools.NumberedChromaticPitchClassColorMap)
    assert isinstance(numbered_chromatic_pitch_class_color_map_2,
        pitchtools.NumberedChromaticPitchClassColorMap)
