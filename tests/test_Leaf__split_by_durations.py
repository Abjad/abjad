import abjad
import pytest


def test_Leaf__split_by_durations_01():
    """
    Splits note into assignable notes.

    Does not fracture spanners. Does not tie split notes.
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
        [abjad.Duration(1, 32)],
        fracture_spanners=False,
        tie_split_notes=False,
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

    Fractures spanners. Does not tie split notes.
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
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'32
            ]
            d'16.
            [
            e'8
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_03():
    """
    Splits note into assignable notes.

    Does not fracture spanners. Does tie split notes.
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
        [abjad.Duration(1, 32)],
        fracture_spanners=False,
        tie_split_notes=True,
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


def test_Leaf__split_by_durations_04():
    """
    Splits note into assignable notes.

    Fractures spanners. Ties split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    new_leaves = staff[1]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            [
            d'32
            ~
            ]
            d'16.
            [
            e'8
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_05():
    """
    Adds tuplet.

    Does not fracture spanners. Does not tie split notes.
    """

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    new_leaves = staff[1]._split_by_durations(
        [abjad.Duration(1, 24)],
        tie_split_notes=False,
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


def test_Leaf__split_by_durations_06():
    """
    REGRESSION.
    
    Splits note into tuplet monads and then fuses monads.

    Does not fracture spanners. Ties split notes.

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
                    ~
                    [
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


def test_Leaf__split_by_durations_07():
    """
    Assignable duration produces two notes.

    This test comes from a container-crossing spanner bug.
    """

    voice = abjad.Voice(r"c'8 \times 2/3 { d'8 e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

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
        [abjad.Duration(1, 24)],
        tie_split_notes=False,
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


def test_Leaf__split_by_durations_08():
    """
    Leaf duration less than split duration produces no change.
    """

    staff = abjad.Staff("c'4")
    staff[0]._split_by_durations([abjad.Duration(3, 4)])

    assert len(staff) == 1
    assert isinstance(staff[0], abjad.Note)
    assert staff[0].written_duration == abjad.Duration(1, 4)


def test_Leaf__split_by_durations_09():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")

    new_leaves = note._split_by_durations(
        [abjad.Duration(1, 8)],
        tie_split_notes=False,
        )

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_10():
    """
    Returns selection of new leaves.
    """

    note = abjad.Note("c'4")
    new_leaves = note._split_by_durations([abjad.Duration(1, 16)])

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_11():
    """
    Nonassignable power-of-two duration returns selection of new leaves.
    """

    note = abjad.Note("c'4")

    new_leaves = note._split_by_durations(
        [abjad.Duration(5, 32)],
        tie_split_notes=False,
        )

    assert isinstance(new_leaves, abjad.Selection)
    assert all(isinstance(_, abjad.Note) for _ in new_leaves)


def test_Leaf__split_by_durations_12():
    """
    Lone spanned leaf results in two spanned leaves.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    tie = abjad.Tie()
    abjad.attach(tie, staff[:])
    new_leaves = staff[0]._split_by_durations([abjad.Duration(1, 8)])

    assert len(staff) == 2
    for leaf in staff[:]:
        assert abjad.inspect(leaf).spanners() == [tie]
        prototype = (abjad.Tie,)
        assert abjad.inspect(leaf).spanner(prototype) is tie

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_13():
    """
    Leaves spanners unchanged.
    """

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])

    new_leaves = staff[0]._split_by_durations(
        [abjad.Duration(1, 16)],
        tie_split_notes=False,
        )

    assert len(staff) == 5
    for l in staff:
        assert abjad.inspect(l).spanners() == [beam]
        assert l._get_spanner(abjad.Beam) is beam

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_14():
    """
    Returns three leaves with two tied.

    Spanner is shared by all 3 leaves.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    tie = abjad.Tie()
    abjad.attach(tie, staff[:])

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


def test_Leaf__split_by_durations_15():
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


def test_Leaf__split_by_durations_16():
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


def test_Leaf__split_by_durations_17():
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


def test_Leaf__split_by_durations_18():

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=False,
        tie_split_notes=False,
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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_19():
    """
    Split one leaf in score.
    Do not fracture spanners. But do tie after split.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam()
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                ~
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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_20():
    """
    Split leaf in score and fracture spanners.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                [
                ]
                c'16.
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_21():
    """
    Split leaf in score at nonzero index.
    Fracture spanners.
    Test comes from a bug fix.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    new_leaves = leaves[1]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
                d'32
                ]
                )
                d'16.
                [
                ]
                (
            }
            {
                e'8
                [
                f'8
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_22():
    """
    Split leaf outside of score and fracture spanners.
    """

    note = abjad.Note("c'8")
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, abjad.select(note))

    assert format(note) == "c'8\n[\n]"

    new_leaves = note._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        )
    staff = abjad.Staff(new_leaves)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'32
            ~
            [
            ]
            c'16.
            [
            ]
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_23():
    """
    Split leaf in score and fracture spanners.
    Tie leaves after split.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[:2])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[-2:])
    slur = abjad.Slur()
    abjad.attach(slur, leaves)

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
                ]
                )
            }
        }
        """
        ), print(format(staff))

    new_leaves = leaves[0]._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                ~
                [
                ]
                c'16.
                [
                (
                d'8
                ]
            }
            {
                e'8
                [
                f'8
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_24():
    """
    Split leaf with LilyPond multiplier.
    Split at split offset with power-of-two denominator.
    new_leaves carry original written duration.
    new_leaves carry adjusted LilyPond multipliers.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert format(note) == "c'8 * 1/2"

    new_leaves = note._split_by_durations(
        [abjad.Duration(1, 32)],
        fracture_spanners=True,
        tie_split_notes=False,
        )

    staff = abjad.Staff(new_leaves)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8 * 1/4
            c'8 * 1/4
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Leaf__split_by_durations_25():
    """
    Split leaf with LilyPond multiplier.
    Split at offset without power-of-two denominator.
    new_leaves carry original written duration.
    new_leaves carry adjusted LilyPond multipliers.
    """

    note = abjad.Note(0, (1, 8), multiplier=(1, 2))

    assert format(note) == "c'8 * 1/2"

    new_leaves = note._split_by_durations(
        [abjad.Duration(1, 48)],
        fracture_spanners=True,
        tie_split_notes=False,
        )

    staff = abjad.Staff(new_leaves)
    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8 * 1/6
            c'8 * 1/3
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
