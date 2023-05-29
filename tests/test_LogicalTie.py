import abjad


def test_LogicalTie_written_duration_01():
    staff = abjad.Staff("c' ~ c'16")

    assert abjad.get.logical_tie(staff[0]).written_duration == abjad.Duration(5, 16)


def test_LogicalTie_written_duration_02():
    staff = abjad.Staff("c'")

    assert abjad.get.logical_tie(staff[0]).written_duration == abjad.Duration(1, 4)
