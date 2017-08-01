# -*- coding: utf-8 -*-
import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__HorizontalBracket_01():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    bracket = abjad.HorizontalBracketSpanner()
    abjad.attach(bracket, target[:])
    bracket = abjad.HorizontalBracketSpanner()
    abjad.attach(bracket, target[:2])
    bracket = abjad.HorizontalBracketSpanner()
    abjad.attach(bracket, target[2:])

    assert format(target) == abjad.String.normalize(
        r'''
        {
            c'4 \startGroup \startGroup
            c'4 \stopGroup
            c'4 \startGroup
            c'4 \stopGroup \stopGroup
        }
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
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
