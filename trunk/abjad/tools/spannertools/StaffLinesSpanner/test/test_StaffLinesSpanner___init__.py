# -*- encoding: utf-8 -*-
from abjad import *


def test_StaffLinesSpanner___init___01():
    r'''Init empty staff lines spanner.
    '''

    spanner = spannertools.StaffLinesSpanner()
    assert isinstance(spanner, spannertools.StaffLinesSpanner)
