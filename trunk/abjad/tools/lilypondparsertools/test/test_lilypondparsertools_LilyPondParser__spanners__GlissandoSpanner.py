# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_01():

    target = Container([Note(0, 1), Note(0, 1)])
    glissando = spannertools.GlissandoSpanner()
    glissando.attach(target[:])
    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_02():

    string = r'{ c \glissando }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__GlissandoSpanner_03():

    string = r'{ \glissando c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')
