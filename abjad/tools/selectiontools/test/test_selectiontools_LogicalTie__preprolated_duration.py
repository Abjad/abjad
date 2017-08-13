import abjad


def test_selectiontools_LogicalTie__preprolated_duration_01():

    staff = abjad.Staff("c' ~ c'16")

    assert abjad.inspect(staff[0]).get_logical_tie()._get_preprolated_duration() \
        == abjad.Duration(5, 16)


def test_selectiontools_LogicalTie__preprolated_duration_02():

    staff = abjad.Staff("c'")

    assert abjad.inspect(staff[0]).get_logical_tie()._get_preprolated_duration() \
        == abjad.Duration(1, 4)
