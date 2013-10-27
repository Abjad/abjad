# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_01():

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.TieSpanner()
    tie.attach(target[:])
    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_02():

    string = r'{ c ~ }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_03():

    string = r'{ ~ c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_04():
    r'''With direction.
    '''

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.TieSpanner(direction=Up)
    tie.attach(target[:])
    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__TieSpanner_05():
    r'''With direction.
    '''

    target = Container([Note(0, 1), Note(0, 1)])
    tie = spannertools.TieSpanner(direction=Down)
    tie.attach(target[:])
    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
