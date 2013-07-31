# -*- encoding: utf-8 -*-
from abjad import *


def test_TrillSpanner___init___01():
    r'''Init empty trill spanner.
    '''

    trill = spannertools.TrillSpanner()
    assert isinstance(trill, spannertools.TrillSpanner)
