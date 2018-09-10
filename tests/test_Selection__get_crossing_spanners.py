import abjad
import pytest


def test_Selection__get_crossing_spanners_01():
    """
    Helper gets spanners that cross in from above.
    """

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(staff).leaves()
    abjad.beam(leaves[2:5])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                e'8
                [
                f'8
            }
            {
                \time 2/8
                g'8
                ]
                a'8
            }
        }
        """
        ), print(format(staff))

    spanners = abjad.select(leaves)._get_crossing_spanners()

    assert len(spanners) == 0
