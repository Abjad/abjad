from abjad import *
import copy


def test_NamedChromaticPitch___deepcopy___01():

    pitch = pitchtools.NamedChromaticPitch(13)
    new = copy.deepcopy(pitch)

    assert new is not pitch
    assert new._accidental is not pitch._accidental
