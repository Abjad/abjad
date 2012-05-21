from abjad import *


def testMelodicObjectDiatonicIntervalSegment___str___01():

    mdi_segment = pitchtools.MelodicDiatonicIntervalSegment([
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('minor', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('major', 2),
        pitchtools.MelodicDiatonicInterval('minor', 2),])

    assert str(mdi_segment) == '<+M2, +M2, +m2, +M2, +M2, +M2, +m2>'
