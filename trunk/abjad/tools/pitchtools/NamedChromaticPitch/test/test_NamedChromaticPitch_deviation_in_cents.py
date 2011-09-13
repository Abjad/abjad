from abjad import *


def test_NamedChromaticPitch_deviation_in_cents_01():
    '''Deviation defaults to None.'''

    p = pitchtools.NamedChromaticPitch('bf', 4)
    assert p.deviation_in_cents is None


def test_NamedChromaticPitch_deviation_in_cents_02():
    '''Deviation can be int or float.'''

    p = pitchtools.NamedChromaticPitch('bf', 4, -31)
    assert p.deviation_in_cents == -31

    p = pitchtools.NamedChromaticPitch('bf', 4, -12.4)
    assert p.deviation_in_cents == -12.4
