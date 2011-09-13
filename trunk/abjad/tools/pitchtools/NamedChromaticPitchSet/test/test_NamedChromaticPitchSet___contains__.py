from abjad import *


def test_NamedChromaticPitchSet___contains___01():
    '''Pitch set containment works as expected.'''

    pset = pitchtools.NamedChromaticPitchSet([12, 14, 18, 19])

    assert pitchtools.NamedChromaticPitch(14) in pset
    assert pitchtools.NamedChromaticPitch(15) not in pset
