# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__Trill_01():
    r'''Successful trills, showing single leaf overlap.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    trill = spannertools.TrillSpanner()
    attach(trill, target[2:])
    trill = spannertools.TrillSpanner()
    attach(trill, target[:3])

    assert format(target) == stringtools.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Trill_02():
    r'''Swapped start and stop.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    trill = spannertools.TrillSpanner()
    attach(trill, target[2:])
    trill = spannertools.TrillSpanner()
    attach(trill, target[:3])

    assert format(target) == stringtools.normalize(
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
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Trill_03():
    r'''Single leaf.
    '''

    string = r'{ c \startTrillSpan \stopTrillSpan c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Trill_04():
    r'''Unterminated.
    '''

    string = r'{ c \startTrillSpan c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Trill_05():
    r'''Unstarted.
    '''

    string = r'{ c c c c \stopTrillSpan }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Trill_06():
    r'''Nested.
    '''

    string = r'{ c \startTrillSpan c \startTrillSpan c \stopTrillSpan c \stopTrillSpan }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
