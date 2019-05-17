import abjad
import pytest


def test_LilyPondParser__spanners__Tie_01():

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:])
    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Tie_02():

    string = r"{ c ~ }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Tie_03():

    string = r"{ ~ c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Tie_04():
    """
    With direction.
    """

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:], direction=abjad.Up)
    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_LilyPondParser__spanners__Tie_05():
    """
    With direction.
    """

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:], direction=abjad.Down)
    parser = abjad.parser.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
