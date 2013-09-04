# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveIndication___int___01():

    assert int(pitchtools.OctaveIndication('')) == 3
    assert int(pitchtools.OctaveIndication(',')) == 2
    assert int(pitchtools.OctaveIndication(',,')) == 1
    assert int(pitchtools.OctaveIndication(',,,')) == 0
    assert int(pitchtools.OctaveIndication("'")) == 4
    assert int(pitchtools.OctaveIndication("''")) == 5
    assert int(pitchtools.OctaveIndication("'''")) == 6
