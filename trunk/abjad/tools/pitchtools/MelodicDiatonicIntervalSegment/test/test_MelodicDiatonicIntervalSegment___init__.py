from abjad import *


def test_MelodicDiatonicIntervalSegment___init___01():
    '''Init with iterable of melodic diatonic interval instances.'''

    mdi_segment = pitchtools.MelodicDiatonicIntervalSegment([
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('minor', 2)])

    assert mdi_segment[0] == pitchtools.MelodicDiatonicInterval('major', 2)
    assert mdi_segment[1] == pitchtools.MelodicDiatonicInterval('major', 2)
    assert mdi_segment[2] == pitchtools.MelodicDiatonicInterval('minor', 2)
    assert mdi_segment[3] == pitchtools.MelodicDiatonicInterval('major', 2)
    assert mdi_segment[4] == pitchtools.MelodicDiatonicInterval('major', 2)
    assert mdi_segment[5] == pitchtools.MelodicDiatonicInterval('major', 2)
    assert mdi_segment[6] == pitchtools.MelodicDiatonicInterval('minor', 2)
