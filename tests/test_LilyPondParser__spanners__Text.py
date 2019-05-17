import abjad
import pytest


def test_LilyPondParser__spanners__Text_01():
    """
    Successful text spanners, showing single leaf overlap.
    """

    maker = abjad.NoteMaker()
    container = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.text_spanner(container[2:])
    abjad.text_spanner(container[:3])

    assert format(container) == abjad.String.normalize(
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
    result = parser(format(container))
    assert format(container) == format(result) and container is not result


def test_LilyPondParser__spanners__Text_02():
    """
    Swapped start and stop.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.text_spanner(target[2:])
    abjad.text_spanner(target[:3])

    assert format(target) == abjad.String.normalize(
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

    string = r"\relative c' { c \startTextSpan c c \startTextSpan \stopTextSpan c \stopTextSpan }"

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


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
