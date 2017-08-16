import abjad


def test_spannertools_StaffLinesSpanner___init___01():
    r'''Initialize empty staff lines spanner.
    '''

    spanner = abjad.StaffLinesSpanner()
    assert isinstance(spanner, abjad.StaffLinesSpanner)
