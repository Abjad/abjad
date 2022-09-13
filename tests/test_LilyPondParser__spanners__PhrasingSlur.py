import pytest

import abjad


def test_LilyPondParser__spanners__PhrasingSlur_01():
    """
    Successful slurs, showing single leaf overlap.
    """

    target = abjad.Container(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.phrasing_slur(target[2:])
    abjad.phrasing_slur(target[:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            \(
            c'4
            c'4
            \)
            \(
            c'4
            \)
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__PhrasingSlur_02():
    """
    Swapped start and stop.
    """

    target = abjad.Container(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.phrasing_slur(target[2:])
    abjad.phrasing_slur(target[:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            \(
            c'4
            c'4
            \)
            \(
            c'4
            \)
        }
        """
    )

    string = r"\relative c' { c \( c c \( \) c \) }"

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__PhrasingSlur_03():
    """
    Single leaf.
    """

    string = r"{ c \( \) c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__PhrasingSlur_04():
    """
    Unterminated.
    """

    string = r"{ c \( c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__PhrasingSlur_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__PhrasingSlur_06():
    """
    Nested.
    """

    string = r"{ c \( c \( c \) c \) }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)
