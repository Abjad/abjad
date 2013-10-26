# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__PhrasingSlurSpanner_01():
    r'''Successful slurs, showing single leaf overlap.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    phrasing_slur = spannertools.PhrasingSlurSpanner()
    phrasing_slur.attach(target[2:])
    phrasing_slur = spannertools.PhrasingSlurSpanner()
    phrasing_slur.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 \(
            c'4
            c'4 \) \(
            c'4 \)
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__PhrasingSlurSpanner_02():
    r'''Swapped start and stop.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    phrasing_slur = spannertools.PhrasingSlurSpanner()
    phrasing_slur.attach(target[2:])
    phrasing_slur = spannertools.PhrasingSlurSpanner()
    phrasing_slur.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 \(
            c'4
            c'4 \) \(
            c'4 \)
        }
        '''
        )

    string = r"\relative c' { c \( c c \( \) c \) }"

    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__PhrasingSlurSpanner_03():
    r'''Single leaf.
    '''

    string = '{ c \( \) c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_04():
    r'''Unterminated.
    '''

    string = '{ c \( c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_05():
    r'''Unstarted.
    '''

    string = '{ c c c c \) }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__PhrasingSlurSpanner_06():
    r'''Nested.
    '''

    string = '{ c \( c \( c \) c \) }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')
