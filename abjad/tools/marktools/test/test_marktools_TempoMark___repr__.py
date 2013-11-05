# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMark___repr___01():
    r'''Tempo mark returns nonempty string repr.
    '''

    repr = marktools.TempoMark((1, 8), 48).__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
