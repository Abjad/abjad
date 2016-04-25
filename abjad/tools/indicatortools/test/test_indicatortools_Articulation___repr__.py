# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Articulation___repr___01():
    r'''Repr of unattached articulation is evaluable.
    '''

    articulation_1 = Articulation('staccato')
    articulation_2 = eval(repr(articulation_1))

    assert isinstance(articulation_1, Articulation)
    assert isinstance(articulation_2, Articulation)
    assert articulation_1 == articulation_2
