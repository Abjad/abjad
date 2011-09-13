from abjad import *


def test_pitchtools_PitchRange___eq___01():

    pr1 = pitchtools.PitchRange(-39, 48)
    pr2 = pitchtools.PitchRange(-39, 48)

    assert pr1 == pr2
    assert not pr1 != pr2


def test_pitchtools_PitchRange___eq___02():

    pr1 = pitchtools.PitchRange(-39, 48)
    pr2 = pitchtools.PitchRange(0, 48)

    assert not pr1 == pr2
    assert pr1 != pr2
