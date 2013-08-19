# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicIntervalSegment___init___01():
    r'''Init with iterable of melodic diatonic interval instances.
    '''

    mdi_segment = pitchtools.NamedMelodicIntervalSegment([
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('minor', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('major', 2),
        pitchtools.NamedMelodicInterval('minor', 2)])

    assert mdi_segment[0] == pitchtools.NamedMelodicInterval('major', 2)
    assert mdi_segment[1] == pitchtools.NamedMelodicInterval('major', 2)
    assert mdi_segment[2] == pitchtools.NamedMelodicInterval('minor', 2)
    assert mdi_segment[3] == pitchtools.NamedMelodicInterval('major', 2)
    assert mdi_segment[4] == pitchtools.NamedMelodicInterval('major', 2)
    assert mdi_segment[5] == pitchtools.NamedMelodicInterval('major', 2)
    assert mdi_segment[6] == pitchtools.NamedMelodicInterval('minor', 2)
