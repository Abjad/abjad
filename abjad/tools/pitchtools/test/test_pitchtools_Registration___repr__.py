# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.pitchtools import *


def test_pitchtools_Registration___repr___01():
    r'''Repr is evaluable.
    '''

    mapping_1 = pitchtools.Registration([('[A0, C4)', 15), ('[C4, C8)', 27)])
    mapping_2 = eval(repr(mapping_1))

    assert isinstance(mapping_1, pitchtools.Registration)
    assert isinstance(mapping_2, pitchtools.Registration)
    assert mapping_1 == mapping_2
