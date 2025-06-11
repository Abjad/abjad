import copy

import abjad


def test_Tuplet___copy___01():
    tuplet_1 = abjad.Tuplet("3:2", "c'8 d'8 e'8")
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
    assert tuplet.ratio == abjad.Ratio(3, 2)
    assert not len(tuplet)


def test_Tuplet___init__02():
    r"""
    Abjad parses LilyPond's \tuplet command.
    """

    voice = abjad.Voice(r"\tuplet 6/4 { c'4 d' e' }")

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \tuplet 6/4
            {
                c'4
                d'4
                e'4
            }
        }
        """
    )
