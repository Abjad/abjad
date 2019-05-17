import abjad
import pytest


def test_Container__split_by_duration_01():

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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32), tie_split_notes=False
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
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_02():
    """
    Split one container in score.
    Adds tie after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 32), tie_split_notes=True
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
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_03():
    """
    Split in-score at split offset with non-power-of-two denominator.
    Does not tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5), tie_split_notes=False
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
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()


def test_Container__split_by_duration_04():
    """
    Split in-score container at split offset with non-power-of-two denominator.
    Does not tie leaves after split.
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

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 5), tie_split_notes=True
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
                )
                ]
            }
        }
        """
    ), print(format(staff))

    assert abjad.inspect(staff).wellformed()
