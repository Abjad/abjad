import pytest

import abjad


def test_LilyPondParser__spanners__HorizontalBracket_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.horizontal_bracket(target[:])
    abjad.horizontal_bracket(target[:2])
    abjad.horizontal_bracket(target[2:])

    assert abjad.lilypond(target) == abjad.String.normalize(
        r"""
        {
            c'4
            \startGroup
            \startGroup
            c'4
            \stopGroup
            c'4
            \startGroup
            c'4
            \stopGroup
            \stopGroup
        }
        """
    )

    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__HorizontalBracket_02():
    """
    Starting and stopping on the same leaf.
    """

    string = r"""{ c \startGroup \stopGroup c c c }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__HorizontalBracket_03():
    """
    One group stopping on a leaf, while another begins on the same leaf.
    """

    string = r"""{ c \startGroup c \stopGroup \startGroup c c \stopGroup }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__HorizontalBracket_04():
    """
    Unterminated.
    """

    string = r"""{ c \startGroup c c c }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__HorizontalBracket_05():
    """
    Unstarted.
    """

    string = r"""{ c c c c \stopGroup }"""
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)
