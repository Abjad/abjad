import pytest

import abjad


def test_LilyPondParser__spanners__Text_01():
    """
    Successful text spanners, showing single leaf overlap.
    """

    container = abjad.Container(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.text_spanner(container[2:])
    abjad.text_spanner(container[:3])

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'4
            \startTextSpan
            c'4
            c'4
            \stopTextSpan
            \startTextSpan
            c'4
            \stopTextSpan
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(container))
    assert (
        abjad.lilypond(container) == abjad.lilypond(result) and container is not result
    )


def test_LilyPondParser__spanners__Text_02():
    """
    Swapped start and stop.
    """

    target = abjad.Container(abjad.makers.make_notes([0] * 4, [(1, 4)]))
    abjad.text_spanner(target[2:])
    abjad.text_spanner(target[:3])

    assert abjad.lilypond(target) == abjad.string.normalize(
        r"""
        {
            c'4
            \startTextSpan
            c'4
            c'4
            \stopTextSpan
            \startTextSpan
            c'4
            \stopTextSpan
        }
        """
    )

    string = (
        r"\relative c' { c \startTextSpan c c \startTextSpan \stopTextSpan c"
        r" \stopTextSpan }"
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Text_03():
    """
    Single leaf.
    """

    string = r"{ c \startTextSpan \stopTextSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Text_04():
    """
    Unterminated.
    """

    string = r"{ c \startTextSpan c c c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Text_05():
    """
    Unstarted.
    """

    string = r"{ c c c c \stopTextSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Text_06():
    """
    Nested.
    """

    string = r"{ c \startTextSpan c \startTextSpan c \stopTextSpan c \stopTextSpan }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)
