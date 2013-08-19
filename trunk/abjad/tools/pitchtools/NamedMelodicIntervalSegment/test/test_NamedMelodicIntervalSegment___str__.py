# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalSegment___str___01():

    mdi_segment = pitchtools.NamedMelodicIntervalSegment([
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('minor', 2),])

    assert str(mdi_segment) == '<+M2, +M2, +m2, +M2, +M2, +M2, +m2>'
