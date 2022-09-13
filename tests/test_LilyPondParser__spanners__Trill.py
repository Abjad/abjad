import pytest

import abjad


def test_LilyPondParser__spanners__Trill_01():
    """
    Successful trills, showing single leaf overlap.
    """

    notes = abjad.makers.make_notes(4 * [0], [(1, 4)])
    target = abjad.Container(notes)
    abjad.trill_spanner(target[2:])
    abjad.trill_spanner(target[:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            \startTrillSpan
            c'4
            c'4
            \stopTrillSpan
            \startTrillSpan
            c'4
            \stopTrillSpan
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Trill_02():
    """
    Swapped start and stop.
    """

    notes = abjad.makers.make_notes(4 * [0], [(1, 4)])
    target = abjad.Container(notes)
    abjad.trill_spanner(target[2:])
    abjad.trill_spanner(target[:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            \startTrillSpan
            c'4
            c'4
            \stopTrillSpan
            \startTrillSpan
            c'4
            \stopTrillSpan
        }
        """
    )

    string = (
        r"\relative c' { c \startTrillSpan c c \startTrillSpan \stopTrillSpan c"
        r" \stopTrillSpan }"
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Trill_03():
    """
    Single leaf.
    """

    string = r"{ c \startTrillSpan \stopTrillSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Trill_04():
    """
    Unterminated.
    """

    string = r"{ c \startTrillSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Trill_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \stopTrillSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Trill_06():
    """
    Nested.
    """

    string = (
        r"{ c \startTrillSpan c \startTrillSpan c \stopTrillSpan c \stopTrillSpan }"
    )
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)
