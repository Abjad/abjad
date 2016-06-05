# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_01():
    r'''Successful slurs, showing single leaf overlap.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    slur = spannertools.PhrasingSlur()
    attach(slur, target[2:])
    slur = spannertools.PhrasingSlur()
    attach(slur, target[:3])

    assert format(target) == stringtools.normalize(
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
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_02():
    r'''Swapped start and stop.
    '''

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    slur = spannertools.PhrasingSlur()
    attach(slur, target[2:])
    slur = spannertools.PhrasingSlur()
    attach(slur, target[:3])

    assert format(target) == stringtools.normalize(
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
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_03():
    r'''Single leaf.
    '''

    string = '{ c \( \) c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_04():
    r'''Unterminated.
    '''

    string = '{ c \( c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_05():
    r'''Unstarted.
    '''

    string = '{ c c c c \) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__PhrasingSlur_06():
    r'''Nested.
    '''

    string = '{ c \( c \( c \) c \) }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
