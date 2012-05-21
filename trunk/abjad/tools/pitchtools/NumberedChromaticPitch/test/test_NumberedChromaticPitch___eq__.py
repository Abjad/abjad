from abjad import *


def testNumberedObjectChromaticPitch___eq___01():

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(12)
    r = pitchtools.NumberedChromaticPitch(13)

    assert p == p
    assert p == q
    assert not p == r

    assert q == p
    assert q == q
    assert not q == r

    assert not r == p
    assert not r == q
    assert r == r
