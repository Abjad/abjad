import abjad
import pytest


def test_LilyPondParser__spanners__HorizontalBracket_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.horizontal_bracket(target[:])
    abjad.horizontal_bracket(target[:2])
    abjad.horizontal_bracket(target[2:])

    assert format(target) == abjad.String.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__HorizontalBracket_02():
    """
    Starting and stopping on the same leaf.
    """

    string = r"""{ c \startGroup \stopGroup c c c }"""
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__HorizontalBracket_03():
    """
    One group stopping on a leaf, while another begins on the same leaf.
    """

    string = r"""{ c \startGroup c \stopGroup \startGroup c c \stopGroup }"""
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__HorizontalBracket_04():
    """
    Unterminated.
    """

    string = r"""{ c \startGroup c c c }"""
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__HorizontalBracket_05():
    """
    Unstarted.
    """

    string = r"""{ c c c c \stopGroup }"""
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
