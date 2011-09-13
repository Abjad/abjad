from abjad import *


def test_StaffLinesSpanner___init___01():
    '''Init empty staff lines spanner.
    '''

    spanner = spannertools.StaffLinesSpanner()
    assert isinstance(spanner, spannertools.StaffLinesSpanner)
