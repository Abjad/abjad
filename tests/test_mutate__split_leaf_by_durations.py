import abjad


def test_mutate__split_leaf_by_durations_01():
    """
    Splits note into assignable notes.

    Does tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'8
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.mutate._split_leaf_by_durations(staff[1], [abjad.Duration(1, 32)])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'32
            ~
            d'16.
            e'8
            ]
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_02():
    """
    REGRESSION.

    Splits note into tuplet monads and then fuses monads.

    Ties split notes.

    This test comes from #272 in GitHub.
    """

    staff = abjad.Staff(r"\times 2/3 { c'8 [ d'8 e'8 ] }")
    leaf = abjad.get.leaf(staff, 0)
    abjad.mutate._split_leaf_by_durations(leaf, [abjad.Duration(1, 20)])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \times 2/3 {
                \times 4/5 {
                    c'16.
                    [
                    ~
                    c'16
                }
                d'8
                e'8
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_03():
    """
    Leaf duration less than split duration produces no change.
    """

    staff = abjad.Staff("c'4")
    abjad.mutate._split_leaf_by_durations(staff[0], [abjad.Duration(3, 4)])

    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    assert staff[0].written_duration == abjad.Duration(1, 4)


def test_mutate__split_leaf_by_durations_04():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")
    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 16)])

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_mutate__split_leaf_by_durations_05():
    """
    Lone spanned leaf results in two spanned leaves.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    abjad.mutate._split_leaf_by_durations(staff[0], [abjad.Duration(1, 8)])

    assert len(staff) == 2
    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_06():
    """
    Returns three leaves with two tied.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    new_leaves = abjad.mutate._split_leaf_by_durations(
        staff[0], [abjad.Duration(5, 32)]
    )

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'32
            ~
            c'16.
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_07():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    after_grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(after_grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 8)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            \afterGrace
            c'8
            {
                c'32
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.get.after_grace_container(new_leaves[0]) is None
    assert len(abjad.get.after_grace_container(new_leaves[1])) == 1
    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_08():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(5, 32)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            ~
            c'32
            ~
            \afterGrace
            c'16.
            {
                c'32
            }
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_09():
    """
    Grace notes are removed from second split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.BeforeGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = abjad.mutate._split_leaf_by_durations(note, [abjad.Duration(1, 16)])
    staff = abjad.Staff(new_leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \grace {
                c'32
            }
            c'16
            ~
            c'8.
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.wf.wellformed(staff)


def test_mutate__split_leaf_by_durations_10():
    """
    Split one leaf in score.
    Ties after split.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    abjad.mutate._split_leaf_by_durations(leaves[0], [abjad.Duration(1, 32)])

    assert abjad.lilypond(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                [
                (
                ~
                c'16.
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                )
                ]
            }
        }
        """
    ), print(abjad.lilypond(staff))

    assert abjad.wf.wellformed(staff)
