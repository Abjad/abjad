import copy

import abjad


def test_Tuplet___copy___01():
    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.override(tuplet_1).NoteHead.color = "#red"

    assert abjad.lilypond(tuplet_1) == abjad.string.normalize(
        r"""
        \override NoteHead.color = #red
        \tuplet 3/2
        {
            c'8
            d'8
            e'8
        }
        \revert NoteHead.color
        """
    )

    tuplet_2 = copy.copy(tuplet_1)

    assert abjad.lilypond(tuplet_2) == abjad.string.normalize(
        r"""
        \override NoteHead.color = #red
        \tuplet 3/2
        {
        }
        \revert NoteHead.color
        """
    )

    assert not len(tuplet_2)


def test_Tuplet___init___01():
    """
    Initializes tuplet from empty input.
    """

    tuplet = abjad.Tuplet()

    assert abjad.lilypond(tuplet) == "\\tuplet 3/2\n{\n}"
    assert tuplet.multiplier == (2, 3)
    assert not len(tuplet)


# TODO: move to test_get_timespan.py
def test_Tuplet_get_timespan_01():
    staff = abjad.Staff(r"c'4 d'4 \tuplet 3/2 { e'4 f'4 g'4 }")
    leaves = abjad.select.leaves(staff)
    score = abjad.Score([staff])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 60)
    abjad.attach(mark, leaves[0])

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=60
                c'4
                d'4
                \tuplet 3/2
                {
                    e'4
                    f'4
                    g'4
                }
            }
        >>
        """
    )

    assert abjad.get.timespan(staff, in_seconds=True) == abjad.Timespan(0, 4)
    assert abjad.get.timespan(staff[0], in_seconds=True) == abjad.Timespan(0, 1)
    assert abjad.get.timespan(staff[1], in_seconds=True) == abjad.Timespan(1, 2)
    assert abjad.get.timespan(staff[-1], in_seconds=True) == abjad.Timespan(2, 4)


def test_Tuplet_set_minimum_denominator_01():
    tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(8)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 10/6
        {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        """
    )

    assert abjad.wf.wellformed(tuplet)


def test_Tuplet_set_minimum_denominator_02():
    tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(16)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 20/12
        {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        """
    )

    assert abjad.wf.wellformed(tuplet)


def test_Tuplet_set_minimum_denominator_03():
    tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
    tuplet.set_minimum_denominator(2)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \tuplet 5/3
        {
            c'4
            d'8
            e'8
            f'4
            g'2
        }
        """
    )

    assert abjad.wf.wellformed(tuplet)
