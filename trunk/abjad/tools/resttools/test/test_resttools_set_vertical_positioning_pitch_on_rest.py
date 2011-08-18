from abjad import *


def test_resttools_set_vertical_positioning_pitch_on_rest_01():
    '''Set vertical positioning pitch to int.
    '''

    r = Rest((1, 4))
    resttools.set_vertical_positioning_pitch_on_rest(r, 0)

    assert isinstance(r._vertical_positioning_pitch, pitchtools.NamedChromaticPitch)
    assert r.format == "c'4 \\rest"


def test_resttools_set_vertical_positioning_pitch_on_rest_02():
    '''Set vertical positioning pitch to named pitch.
    '''

    r = Rest((1, 4))
    resttools.set_vertical_positioning_pitch_on_rest(r, pitchtools.NamedChromaticPitch(0))

    assert isinstance(r._vertical_positioning_pitch, pitchtools.NamedChromaticPitch)
    assert r.format == "c'4 \\rest"


def test_resttools_set_vertical_positioning_pitch_on_rest_03():
    '''Set vertical positioning pitch to none.
    '''

    r = Rest((1, 4))
    resttools.set_vertical_positioning_pitch_on_rest(r, None)

    assert isinstance(r._vertical_positioning_pitch, type(None))
    assert r.format == "r4"
