# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_StaffLinesSpanner___init___01():
    r'''Initialize empty staff lines spanner.
    '''

    spanner = spannertools.StaffLinesSpanner()
    assert isinstance(spanner, spannertools.StaffLinesSpanner)
