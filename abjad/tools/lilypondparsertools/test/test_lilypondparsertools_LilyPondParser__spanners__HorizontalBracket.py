# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_01():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    bracket = spannertools.HorizontalBracketSpanner()
    attach(bracket, target[:])
    bracket = spannertools.HorizontalBracketSpanner()
    attach(bracket, target[:2])
    bracket = spannertools.HorizontalBracketSpanner()
    attach(bracket, target[2:])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4 \startGroup \startGroup
            c'4 \stopGroup
            c'4 \startGroup
            c'4 \stopGroup \stopGroup
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_02():
    r'''Starting and stopping on the same leaf.
    '''

    string = r'''{ c \startGroup \stopGroup c c c }'''
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_03():
    r'''One group stopping on a leaf, while another begins on the same leaf.
    '''

    string = r'''{ c \startGroup c \stopGroup \startGroup c c \stopGroup }'''
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_04():
    r'''Unterminated.
    '''

    string = r'''{ c \startGroup c c c }'''
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_05():
    r'''Unstarted.
    '''

    string = r'''{ c c c c \stopGroup }'''
    assert pytest.raises(Exception, 'LilyPondParser()(string)')
