import pytest

import abjad


def test_LilyPondParser__spanners__Tie_01():

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:])
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


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
    abjad.tie(target[:], direction=abjad.UP)
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Tie_05():
    """
    With direction.
    """

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.tie(target[:], direction=abjad.DOWN)
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result
