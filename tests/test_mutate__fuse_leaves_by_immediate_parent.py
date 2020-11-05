import abjad


def test_mutate__fuse_leaves_by_immediate_parent_01():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff([abjad.Container("c'8 c'8"), abjad.Container("c'8 c'8")])
    leaves = abjad.select(staff).leaves()
    abjad.tie(leaves)

    logical_tie = abjad.get.logical_tie(leaves[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    assert len(result) == 2
    assert abjad.wf.wellformed(staff)


def test_mutate__fuse_leaves_by_immediate_parent_02():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    abjad.tie(staff[:])

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    ), print(abjad.lilypond(staff))

    logical_tie = abjad.get.logical_tie(staff[1])
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'2
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
    assert len(result) == 1


def test_mutate__fuse_leaves_by_immediate_parent_03():
    """
    Fuse leaves in logical tie with same immediate parent.
    """

    note = abjad.Note("c'4")
    logical_tie = abjad.get.logical_tie(note)
    result = abjad.mutate._fuse_leaves_by_immediate_parent(logical_tie)
    assert len(result) == 1
    assert abjad.wf.wellformed(note)
