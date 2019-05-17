import abjad
import pytest


def test_LilyPondParser__spanners__Slur_01():
    """
    Successful slurs, showing single leaf overlap.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.slur(target[2:])
    abjad.slur(target[:3])

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'4
            (
            c'4
            c'4
            )
            (
            c'4
            )
        }
        """
        )

    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Slur_02():
    """
    Swapped start and stop.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    abjad.slur(target[2:])
    abjad.slur(target[:3])

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'4
            (
            c'4
            c'4
            )
            (
            c'4
            )
        }
        """
        )

    string = r"\relative c' { c ( c c () c ) }"

    parser = abjad.parser.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Slur_03():
    """
    Single leaf.
    """

    string = '{ c () c c c }'
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Slur_04():
    """
    Unterminated.
    """

    string = '{ c ( c c c }'
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Slur_05():
    """
    Unstarted.
    """

    string = '{ c c c c ) }'
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Slur_06():
    """
    Nested.
    """

    string = '{ c ( c ( c ) c ) }'
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Slur_07():
    """
    With direction.
    """

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    start_slur = abjad.StartSlur(direction=abjad.Down)
    abjad.slur(target[:3], start_slur=start_slur)
    start_slur = abjad.StartSlur(direction=abjad.Up)
    abjad.slur(target[2:], start_slur=start_slur)

    assert format(target) == abjad.String.normalize(
        r"""
        {
            c'4
            _ (
            c'4
            c'4
            )
            ^ (
            c'4
            )
        }
        """
        )

    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
