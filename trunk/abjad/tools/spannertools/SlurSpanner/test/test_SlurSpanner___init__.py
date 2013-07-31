# -*- encoding: utf-8 -*-
from abjad import *


def test_SlurSpanner___init___01():
    r'''Init empty slur spanner.
    '''

    slur = spannertools.SlurSpanner()
    assert isinstance(slur, spannertools.SlurSpanner)
