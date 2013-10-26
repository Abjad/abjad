# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__SlurSpanner_01():
    r'''Successful slurs, showing single leaf overlap.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    slur = spannertools.SlurSpanner()
    slur.attach(target[2:])
    slur = spannertools.SlurSpanner()
    slur.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__SlurSpanner_02():
    r'''Swapped start and stop.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    slur = spannertools.SlurSpanner()
    slur.attach(target[2:])
    slur = spannertools.SlurSpanner()
    slur.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 (
            c'4
            c'4 ) (
            c'4 )
        }
        '''
        )

    string = r"\relative c' { c ( c c () c ) }"

    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__SlurSpanner_03():
    r'''Single leaf.
    '''

    string = '{ c () c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__SlurSpanner_04():
    r'''Unterminated.
    '''

    string = '{ c ( c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__SlurSpanner_05():
    r'''Unstarted.
    '''

    string = '{ c c c c ) }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__SlurSpanner_06():
    r'''Nested.
    '''

    string = '{ c ( c ( c ) c ) }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__SlurSpanner_07():
    r'''With direction.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    slur = spannertools.SlurSpanner(direction=Down)
    slur.attach(target[:3])
    slur = spannertools.SlurSpanner(direction=Up)
    slur.attach(target[2:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 _ (
            c'4
            c'4 ) ^ (
            c'4 )
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result
