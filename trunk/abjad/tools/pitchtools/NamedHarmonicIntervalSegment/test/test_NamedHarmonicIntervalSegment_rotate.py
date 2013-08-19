# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicIntervalSegment_rotate_01():
    r'''Rotate right.
    '''

    hdig = pitchtools.NamedHarmonicIntervalSegment([
        pitchtools.NamedHarmonicInterval('minor', 2),
        pitchtools.NamedHarmonicInterval('major', 2),
        pitchtools.NamedHarmonicInterval('minor', 3),
        pitchtools.NamedHarmonicInterval('major', 3)])

    rotated = hdig.rotate(1)

    new = pitchtools.NamedHarmonicIntervalSegment([
        pitchtools.NamedHarmonicInterval('major', 3),
        pitchtools.NamedHarmonicInterval('minor', 2),
        pitchtools.NamedHarmonicInterval('major', 2),
        pitchtools.NamedHarmonicInterval('minor', 3)])

    assert rotated == new


def test_NamedHarmonicIntervalSegment_rotate_02():
    r'''Rotate left.
    '''

    hdig = pitchtools.NamedHarmonicIntervalSegment([
        pitchtools.NamedHarmonicInterval('minor', 2),
        pitchtools.NamedHarmonicInterval('major', 2),
        pitchtools.NamedHarmonicInterval('minor', 3),
        pitchtools.NamedHarmonicInterval('major', 3)])

    rotated = hdig.rotate(-1)

    new = pitchtools.NamedHarmonicIntervalSegment([
        pitchtools.NamedHarmonicInterval('major', 2),
        pitchtools.NamedHarmonicInterval('minor', 3),
        pitchtools.NamedHarmonicInterval('major', 3),
        pitchtools.NamedHarmonicInterval('minor', 2)])

    assert rotated == new
