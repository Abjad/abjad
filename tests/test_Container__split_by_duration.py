import abjad
import pytest


def test_Container__split_by_duration_01():

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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
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
            }
            {
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


def test_Container__split_by_duration_02():
    """
    Split one container in score.
    Do not fracture spanners. But do add tie after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
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
            }
            {
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


def test_Container__split_by_duration_03():
    """
    Split in-score at split offset with non-power-of-two denominator. Do not
    fracture spanners and do not tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=False,
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
            }
            {
                \times 4/5 {
                    d'16.
                    d'16
                    ]
                }
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


def test_Container__split_by_duration_04():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    Do fracture spanners and do tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
            }
            {
                \times 4/5 {
                    d'16.
                    ~
                    d'16
                    ]
                }
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


def test_Container__split_by_duration_05():
    """
    Split container in score and fracture spanners.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
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
            }
            {
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


def test_Container__split_by_duration_06():
    """
    Split staff outside of score and fracture spanners.
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

    halves = staff._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(halves[0][0]) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'32
                [
                ]
            }
        }
        """
        ), print(format(halves[0][0]))

    assert format(halves[1][0]) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
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
        ), print(format(halves[1][0]))


def test_Container__split_by_duration_07():
    """
    Split container over leaf at nonzero index.
    Fracture spanners.
    Test results from bug fix.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(7, 32),
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
                d'16.
                ]
                )
            }
            {
                d'32
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


def test_Container__split_by_duration_08():
    """
    Split container between leaves and fracture spanners.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 8),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                ]
            }
            {
                d'8
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


def test_Container__split_by_duration_09():
    """
    Split container in score and fracture spanners.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32),
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
            }
            {
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


def test_Container__split_by_duration_10():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    Do fracture spanners but do not tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
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
            }
            {
                \times 4/5 {
                    d'16.
                    ]
                    )
                    d'16
                    [
                    ]
                    (
                }
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


def test_Container__split_by_duration_11():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    Do fracture spanners and do tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5),
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
            }
            {
                \times 4/5 {
                    d'16.
                    ~
                    ]
                    )
                    d'16
                    [
                    ]
                    (
                }
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


def test_Container__split_by_duration_12():
    """
    Split container at split offset with non-power-of-two denominator. Do
    fracture spanners but do not tie across split locus. This test results from
    a fix. What's being tested here is contents rederivation.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8 e'8"))
    staff.append(abjad.Container("c'8 d'8 e'8"))
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[:3])
    beam = abjad.Beam(beam_lone_notes=True)
    abjad.attach(beam, leaves[-3:])
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
                e'8
                ]
            }
            {
                c'8
                [
                d'8
                e'8
                ]
                )
            }
        }
        """
        ), print(format(staff))

    halves = staff[0]._split_by_duration(
        abjad.Duration(7, 20),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8
                [
                (
                d'8
            }
            {
                \times 4/5 {
                    e'8
                    ~
                    ]
                    )
                    e'32
                    [
                    ]
                    (
                }
            }
            {
                c'8
                [
                d'8
                e'8
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_13():
    """
    Split container with multiplied leaves. Split at between-leaf offset with
    power-of-two denominator. Leaves remain unaltered.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        leaf.multiplier = (1, 2)
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
                c'8 * 1/2
                [
                (
                d'8 * 1/2
                ]
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 16),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8 * 1/2
                [
                ]
            }
            {
                d'8 * 1/2
                [
                ]
                (
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_14():
    """
    Split container with multiplied leaves. Split at through-leaf offset with
    power-of-two denominator. Leaf written durations stay the same but
    multipliers change.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        leaf.multiplier = (1, 2)
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
                c'8 * 1/2
                [
                (
                d'8 * 1/2
                ]
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    halves = staff[0]._split_by_duration(
        abjad.Duration(3, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8 * 1/2
                [
                (
                d'8 * 1/4
                ]
                )
            }
            {
                d'8 * 1/4
                [
                ]
                (
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_15():
    """
    Split container with multiplied leaves. Split at through-leaf offset
    with non-power-of-two denominator. Leaf written durations adjust for change
    from power-of-two denominator to non-power-of-two denominator. Leaf
    multipliers also change.
    """

    staff = abjad.Staff()
    staff.append(abjad.Container("c'8 d'8"))
    staff.append(abjad.Container("e'8 f'8"))
    leaves = abjad.select(staff).leaves()
    for leaf in leaves:
        leaf.multiplier = (1, 2)
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
                c'8 * 1/2
                [
                (
                d'8 * 1/2
                ]
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    halves = staff[0]._split_by_duration(
        abjad.Duration(2, 24),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                c'8 * 1/2
                [
                (
                d'8 * 1/6
                ]
                )
            }
            {
                d'8 * 1/3
                [
                ]
                (
            }
            {
                e'8 * 1/2
                [
                f'8 * 1/2
                ]
                )
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_16():
    """
    Split container with multiplied leaves. Split at through-leaf offset
    with non-power-of-two denominator.
    """

    staff = abjad.Staff([abjad.Container("s1 * 5/16")])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                s1 * 5/16
            }
        }
        """
        ), print(format(staff))

    halves = staff[0]._split_by_duration(
        abjad.Duration(16, 80),
        fracture_spanners=True,
        )

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                s1 * 1/5
            }
            {
                s1 * 9/80
            }
        }
        """
        ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_17():
    """
    Make sure tie (re)application happens only where sensible.
    """

    halves = abjad.Container("c'4")._split_by_duration(
        abjad.Duration(3, 16),
        fracture_spanners=True,
        )

    assert format(halves[0][0]) == abjad.String.normalize(
        r"""
        {
            c'8.
        }
        """
        ), print(format(halves[0][0]))

    assert format(halves[-1][0]) == abjad.String.normalize(
        r"""
        {
            c'16
        }
        """
        ), print(format(halves[-1][0]))

    assert abjad.inspect(halves[0][0]).wellformed()
    assert abjad.inspect(halves[-1][0]).wellformed()
