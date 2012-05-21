from abjad import *
import py.test


def test_pitchtoolsPitchObjectRange___setattr___01():
    '''Pitch ranges are immutable.
    '''

    pitch_range = pitchtools.PitchRange(-12, 36)

    assert py.test.raises(AttributeError, "pitch_range.foo = 'bar'")
