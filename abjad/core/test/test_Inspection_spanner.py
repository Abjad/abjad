import abjad
import pytest


def test_Inspection_spanner_01():

    container = abjad.Container("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, container[:-1])
    slur = abjad.Slur()
    abjad.attach(slur, container[:-1])

    assert format(container) == abjad.String.normalize(
        r"""
        {
            c'8
            [
            (
            d'8
            e'8
            ]
            )
            f'8
        }
        """
        )

    string = 'inspect(container[0]).spanner()'
    assert pytest.raises(Exception, string)

    assert abjad.inspect(container[-1]).spanner() is None


def test_Inspection_spanner_02():

    staff = abjad.Staff(r"c'4 \times 2/3 { d'8 e'8 f'8 } g'2")
    leaves = abjad.select(staff).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, leaves)
    for leaf in leaves:
        assert slur == abjad.inspect(leaf).spanner(abjad.Slur)
