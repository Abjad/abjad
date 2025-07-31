import abjad


def test_Component__sibling_01():
    """
    Returns component when index is in range.
    """

    staff = abjad.Staff("c' d' e' f'")
    assert staff[1]._sibling(1) is staff[2]
    assert staff[1]._sibling(-1) is staff[0]


def test_Component__sibling_02():
    """
    Returns none when component has no parent.
    """

    staff = abjad.Staff("c' d' e' f'")
    assert staff._sibling(1) is None


def test_Component__sibling_03():
    staff = abjad.Staff(r"c'4 \tuplet 3/2 { d'8 e'8 f'8 } g'2")

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            \tuplet 3/2
            {
                d'8
                e'8
                f'8
            }
            g'2
        }
        """
    )

    leaves = abjad.select.leaves(staff)
    tuplet = staff[1]

    assert leaves[0]._sibling(-1) is None
    assert leaves[0]._sibling(1) is tuplet

    assert tuplet._sibling(-1) is leaves[0]
    assert tuplet._sibling(1) is leaves[4]

    assert leaves[1]._sibling(-1) is leaves[0]
    assert leaves[1]._sibling(1) is leaves[2]
