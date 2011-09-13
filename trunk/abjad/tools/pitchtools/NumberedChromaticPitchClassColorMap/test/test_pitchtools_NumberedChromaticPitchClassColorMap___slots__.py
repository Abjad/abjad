from abjad import *
import py.test


def test_pitchtools_NumberedChromaticPitchClassColorMap___slots___01():
    '''Numbered chromatic pitch-class color maps are immutable.
    '''

    pitches = [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    colors = ['red', 'green', 'blue']
    numbered_chromatic_pitch_class_color_map = pitchtools.NumberedChromaticPitchClassColorMap(
        pitches, colors)

    assert py.test.raises(AttributeError, "numbered_chromatic_pitch_class_color_map.foo = 'bar'")
