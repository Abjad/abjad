import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Glissando_01():

    target = abjad.Container([abjad.Note(0, 1), abjad.Note(0, 1)])
    glissando = abjad.Glissando()
    abjad.attach(glissando, target[:])
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Glissando_02():

    string = r'{ c \glissando }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Glissando_03():

    string = r'{ \glissando c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
