import abjad


def test_LogicalTie_leaves_01():

    staff = abjad.Staff("c' ~ c'16")

    assert abjad.get.logical_tie(staff[0]).leaves == tuple(staff[:])


def test_LogicalTie_leaves_02():

    staff = abjad.Staff("c'")

    assert abjad.get.logical_tie(staff[0]).leaves == (staff[0],)
