import abjad
import pytest


def test_Leaf__split_by_durations_01():
    """
    Splits note into assignable notes.

    Does not tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    new_leaves = staff[1]._split_by_durations(
        [abjad.Duration(1, 32)], tie_split_notes=False
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'32
            d'16.
            e'8
            ]
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_02():
    """
    Splits note into assignable notes.

    Does tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    new_leaves = staff[1]._split_by_durations(
        [abjad.Duration(1, 32)], tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_03():
    """
    Adds tuplet.

    Does not tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    new_leaves = staff[1]._split_by_durations(
        [abjad.Duration(1, 24)], tie_split_notes=False
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            \times 2/3 {
                d'16
                d'8
            }
            e'8
            ]
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_04():
    """
    REGRESSION.
    
    Splits note into tuplet monads and then fuses monads.

    Ties split notes.

    This test comes from #272 in GitHub.
    """

    staff = abjad.Staff(r"\times 2/3 { c'8 [ d'8 e'8 ] }")
    leaf = abjad.inspect(staff).leaf(0)
    new_leaves = leaf._split_by_durations([abjad.Duration(1, 20)])

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_05():
    """
    Assignable duration produces two notes.
    """

    voice = abjad.Voice(r"c'8 \times 2/3 { d'8 e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    abjad.beam(leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \times 2/3 {
                d'8
                e'8
                f'8
                ]
            }
        }
        """
    ), print(format(staff))

    new_leaves = leaves[1]._split_by_durations(
        [abjad.Duration(1, 24)], tie_split_notes=False
    )

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \times 2/3 {
                d'16
                d'16
                e'8
                f'8
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(voice).wellformed()


def test_Leaf__split_by_durations_06():
    """
    Leaf duration less than split duration produces no change.
    """

    staff = abjad.Staff("c'4")
    staff[0]._split_by_durations([abjad.Duration(3, 4)])

    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    assert staff[0].written_duration == abjad.Duration(1, 4)


def test_Leaf__split_by_durations_07():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")

    new_leaves = note._split_by_durations(
        [abjad.Duration(1, 8)], tie_split_notes=False
    )

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_08():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")
    new_leaves = note._split_by_durations([abjad.Duration(1, 16)])

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_09():
    """
    Nonassignable power-of-two duration returns selection of new leaves.
    """

    note = abjad.Note("c'4")

    new_leaves = note._split_by_durations(
        [abjad.Duration(5, 32)], tie_split_notes=False
    )

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_10():
    """
    Lone spanned leaf results in two spanned leaves.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    new_leaves = staff[0]._split_by_durations([abjad.Duration(1, 8)])

    assert len(staff) == 2
    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_11():

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    abjad.beam(staff[:])

    new_leaves = staff[0]._split_by_durations(
        [abjad.Duration(1, 16)], tie_split_notes=False
    )

    assert len(staff) == 5
    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_12():
    """
    Returns three leaves with two tied.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    new_leaves = staff[0]._split_by_durations([abjad.Duration(5, 32)])

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_13():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    after_grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(after_grace, note)

    new_leaves = note._split_by_durations([abjad.Duration(1, 8)])
    staff = abjad.Staff(new_leaves)

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    assert abjad.inspect(new_leaves[0]).after_grace_container() is None
    assert len(abjad.inspect(new_leaves[1]).after_grace_container()) == 1
    abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_14():
    """
    After grace notes are removed from first split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = note._split_by_durations([abjad.Duration(5, 32)])
    staff = abjad.Staff(new_leaves)

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_15():
    """
    Grace notes are removed from second split leaf.
    """

    note = abjad.Note("c'4")
    grace = abjad.GraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)

    new_leaves = note._split_by_durations([abjad.Duration(1, 16)])
    staff = abjad.Staff(new_leaves)

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_16():

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[:2])
    abjad.beam(leaves[-2:])
    abjad.slur(leaves)

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)], tie_split_notes=False
    )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                [
                (
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
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_17():
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

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)], tie_split_notes=True
    )

    assert format(staff) == abjad.String.normalize(
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
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
