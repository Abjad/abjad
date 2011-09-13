from abjad import *
import copy


def test_NamedChromaticPitch___copy___01():

    pitch = pitchtools.NamedChromaticPitch(13)
    new = copy.copy(pitch)

    assert new is not pitch
    assert new._accidental is not pitch._accidental
