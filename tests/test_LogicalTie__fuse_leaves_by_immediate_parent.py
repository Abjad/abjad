import abjad


def test_LogicalTie__fuse_leaves_by_immediate_parent_01():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff(2 * abjad.Container("c'8 c'8"))
    leaves = abjad.select(staff).leaves()
    abjad.tie(leaves)

    logical_tie = abjad.inspect(leaves[1]).logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'4
                ~
            }
            {
                c'4
            }
        }
        """
        ), print(format(staff))

    assert len(result) == 2
    assert abjad.inspect(staff).wellformed()


def test_LogicalTie__fuse_leaves_by_immediate_parent_02():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    abjad.tie(staff[:])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'8
            ~
            c'8
            ~
            c'8
        }
        """
        ), print(format(staff))

    logical_tie = abjad.inspect(staff[1]).logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
    assert len(result) == 1


def test_LogicalTie__fuse_leaves_by_immediate_parent_03():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    note = abjad.Note("c'4")
    logical_tie = abjad.inspect(note).logical_tie()
    result = logical_tie._fuse_leaves_by_immediate_parent()
    assert len(result) == 1
    assert abjad.inspect(note).wellformed()
