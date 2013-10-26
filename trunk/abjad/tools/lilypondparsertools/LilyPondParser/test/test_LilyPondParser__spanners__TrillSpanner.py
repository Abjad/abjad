# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__spanners__TrillSpanner_01():
    r'''Successful trills, showing single leaf overlap.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    trill = spannertools.TrillSpanner()
    trill.attach(target[2:])
    trill = spannertools.TrillSpanner()
    trill.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 \startTrillSpan
            c'4
            c'4 \stopTrillSpan \startTrillSpan
            c'4 \stopTrillSpan
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(target.lilypond_format)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__TrillSpanner_02():
    r'''Swapped start and stop.
    '''

    target = Container(notetools.make_notes([0] * 4, [(1, 4)]))
    trill = spannertools.TrillSpanner()
    trill.attach(target[2:])
    trill = spannertools.TrillSpanner()
    trill.attach(target[:3])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 \startTrillSpan
            c'4
            c'4 \stopTrillSpan \startTrillSpan
            c'4 \stopTrillSpan
        }
        '''
        )

    string = r"\relative c' { c \startTrillSpan c c \startTrillSpan \stopTrillSpan c \stopTrillSpan }"

    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and target is not result


def test_LilyPondParser__spanners__TrillSpanner_03():
    r'''Single leaf.
    '''

    string = r'{ c \startTrillSpan \stopTrillSpan c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__TrillSpanner_04():
    r'''Unterminated.
    '''

    string = r'{ c \startTrillSpan c c c }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__TrillSpanner_05():
    r'''Unstarted.
    '''

    string = r'{ c c c c \stopTrillSpan }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')


def test_LilyPondParser__spanners__TrillSpanner_06():
    r'''Nested.
    '''

    string = r'{ c \startTrillSpan c \startTrillSpan c \stopTrillSpan c \stopTrillSpan }'
    assert py.test.raises(Exception, 'LilyPondParser()(string)')
