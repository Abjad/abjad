import copy

import abjad


def test_Tuplet___copy___01():

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.override(tuplet_1).NoteHead.color = "#red"

    assert abjad.lilypond(tuplet_1) == abjad.string.normalize(
        r"""
        \override NoteHead.color = #red
        \times 2/3
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
        \times 2/3
        {
        }
        \revert NoteHead.color
        """
    )

    assert not len(tuplet_2)
