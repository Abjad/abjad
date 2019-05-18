import abjad


def test_LogicalTie__add_or_remove_notes_to_achieve_written_duration_01():
    """
    Change trivial logical tie to nontrivial logical tie.
    """

    staff = abjad.Staff("c'8 [ ]")
    logical_tie = abjad.inspect(staff[0]).logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(
        abjad.Duration(5, 32)
    )

    assert abjad.inspect(staff).wellformed()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            ]
            ~
            c'32
            [
            ]
        }
        """
    ), print(format(staff))


def test_LogicalTie__add_or_remove_notes_to_achieve_written_duration_02():
    """
    Change nontrivial logical tie to trivial logical tie.
    """

    staff = abjad.Staff("c'8 ~ [ c'32 ]")
    logical_tie = abjad.inspect(staff[0]).logical_tie()
    logical_tie._add_or_remove_notes_to_achieve_written_duration(
        abjad.Duration(1, 8)
    )

    assert abjad.inspect(staff).wellformed()
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
        }
        """
    ), print(format(staff))
