import pytest

import abjad


def test_LilyPondParser__spanners__Glissando_01():
    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    abjad.glissando(target[:])
    parser = abjad.parser.LilyPondParser()
    result = parser(abjad.lilypond(target))
    assert abjad.lilypond(target) == abjad.lilypond(result) and target is not result


def test_LilyPondParser__spanners__Glissando_02():
    string = r"{ c \glissando }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)


def test_LilyPondParser__spanners__Glissando_03():
    string = r"{ \glissando c }"
    with pytest.raises(Exception):
        abjad.LilyPondParser()(string)
