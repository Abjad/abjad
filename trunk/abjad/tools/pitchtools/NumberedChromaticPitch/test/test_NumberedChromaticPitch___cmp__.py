from abjad import *


def testNumberedObjectChromaticPitch___cmp___01():

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(12)

    assert not p <  q
    assert      p <= q
    assert      p == q
    assert not p != q
    assert not p >  q
    assert      p >= q


def testNumberedObjectChromaticPitch___cmp___02():

    p = pitchtools.NumberedChromaticPitch(12)
    q = pitchtools.NumberedChromaticPitch(13)

    assert not q <  p
    assert not q <= p
    assert not q == p
    assert      q != p
    assert      q >  p
    assert      q >= p


def testNumberedObjectChromaticPitch___cmp___03():

    p = pitchtools.NumberedChromaticPitch(12)
    q = 12

    assert not p <  q
    assert      p <= q
    assert      p == q
    assert not p != q
    assert not p >  q
    assert      p >= q


def testNumberedObjectChromaticPitch___cmp___04():

    p = pitchtools.NumberedChromaticPitch(12)
    q = 13

    assert not q <  p
    assert not q <= p
    assert not q == p
    assert      q != p
    assert      q >  p
    assert      q >= p
