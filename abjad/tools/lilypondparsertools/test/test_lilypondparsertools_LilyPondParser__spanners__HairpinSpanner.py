# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_01():

    target = Staff(scoretools.make_notes([0] * 5, [(1, 4)]))
    hairpin = HairpinSpanner(descriptor='<')
    attach(hairpin, target[:3])
    hairpin = HairpinSpanner(descriptor='>')
    attach(hairpin, target[2:])
    dynamic = DynamicMark('ppp')
    attach(dynamic, target[-1])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            c'4 \<
            c'4
            c'4 \! \>
            c'4
            c'4 \ppp
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_02():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    hairpin = HairpinSpanner(descriptor='<')
    attach(hairpin, target[0:2])
    hairpin = HairpinSpanner(descriptor='<')
    attach(hairpin, target[1:3])
    hairpin = HairpinSpanner(descriptor='<')
    attach(hairpin, target[2:])

    assert testtools.compare(
        target,
        r'''
        {
            c'4 \<
            c'4 \! \<
            c'4 \! \<
            c'4 \!
        }
        '''
        )

    input = r'''\relative c' { c \< c \< c \< c \! }'''
    parser = LilyPondParser()
    result = parser(input)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_03():
    r'''Dynamic marks can terminate hairpins.
    '''

    target = Staff(scoretools.make_notes([0] * 3, [(1, 4)]))
    hairpin = HairpinSpanner(descriptor='<')
    attach(hairpin, target[0:2])
    hairpin = HairpinSpanner(descriptor='>')
    attach(hairpin, target[1:])
    dynamic = DynamicMark('p')
    attach(dynamic, target[1])
    dynamic = DynamicMark('f')
    attach(dynamic, target[-1])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            c'4 \<
            c'4 \p \>
            c'4 \f
        }
        '''
        )

    input = r"\new Staff \relative c' { c \< c \p \> c \f }"
    parser = LilyPondParser()
    result = parser(input)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_04():
    r'''Unterminated.
    '''

    string = r'{ c \< c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_05():
    r'''Unbegun is okay.
    '''

    string = r'{ c c c c \! }'
    result = LilyPondParser()(string)


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_06():
    r'''No double dynamic spans permitted.
    '''

    string = r'{ c \< \> c c c \! }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__HairpinSpanner_07():
    r'''With direction.
    '''

    target = Staff(scoretools.make_notes([0] * 5, [(1, 4)]))
    hairpin = HairpinSpanner(descriptor='<', direction=Up)
    attach(hairpin, target[:3])
    hairpin = HairpinSpanner(descriptor='>', direction=Down)
    attach(hairpin, target[2:])
    dynamic = DynamicMark('ppp')
    attach(dynamic, target[-1])

    assert testtools.compare(
        target,
        r'''
        \new Staff {
            c'4 ^ \<
            c'4
            c'4 \! _ \>
            c'4
            c'4 \ppp
        }
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
