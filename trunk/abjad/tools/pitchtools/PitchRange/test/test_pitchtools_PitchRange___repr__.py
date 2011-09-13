from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitch
from abjad.tools.pitchtools import PitchRange


def test_pitchtools_PitchRange___repr___01():
    '''Pitch range reprs are evaluable.
    '''

    pitch_range_1 = pitchtools.PitchRange(-12, 36)
    pitch_range_2 = eval(repr(pitch_range_1))

    assert isinstance(pitch_range_1, PitchRange)
    assert isinstance(pitch_range_2, PitchRange)

    assert pitch_range_1 == pitch_range_2
    assert not pitch_range_1 is pitch_range_2
