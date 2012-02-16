import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__GlissandoSpanner_01():
    target = Container([Note(0, 1), Note(0, 1)])
    spannertools.GlissandoSpanner(target[:])
    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result


def test_LilyPondParser__spanners__GlissandoSpanner_02():
    input = r'{ c \glissando }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')


def test_LilyPondParser__spanners__GlissandoSpanner_03():
    input = r'{ \glissando c }'
    assert py.test.raises(Exception, 'LilyPondParser()(input)')
