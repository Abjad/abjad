# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_01():

    target = Staff(scoretools.make_notes([0] * 5, [(1, 4)]))
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, target[:3])
    hairpin = Hairpin(descriptor='>')
    attach(hairpin, target[2:])
    dynamic = Dynamic('ppp')
    attach(dynamic, target[-1])

    assert format(target) == stringtools.normalize(
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


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_02():

    target = Container(scoretools.make_notes([0] * 4, [(1, 4)]))
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, target[0:2])
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, target[1:3])
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, target[2:])

    assert format(target) == stringtools.normalize(
        r'''
        {
            c'4 \<
            c'4 \! \<
            c'4 \! \<
            c'4 \!
        }
        '''
        )

    string = r'''\relative c' { c \< c \< c \< c \! }'''
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_03():
    r'''Dynamics can terminate hairpins.
    '''

    target = Staff(scoretools.make_notes([0] * 3, [(1, 4)]))
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, target[0:2])
    hairpin = Hairpin(descriptor='>')
    attach(hairpin, target[1:])
    dynamic = Dynamic('p')
    attach(dynamic, target[1])
    dynamic = Dynamic('f')
    attach(dynamic, target[-1])

    assert format(target) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 \<
            c'4 \p \>
            c'4 \f
        }
        '''
        )

    string = r"\new Staff \relative c' { c \< c \p \> c \f }"
    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_04():
    r'''Unterminated.
    '''

    string = r'{ c \< c c c }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_05():
    r'''Unbegun is okay.
    '''

    string = r'{ c c c c \! }'
    result = LilyPondParser()(string)


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_06():
    r'''No double dynamic spans permitted.
    '''

    string = r'{ c \< \> c c c \! }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_07():
    r'''With direction.
    '''

    target = Staff(scoretools.make_notes([0] * 5, [(1, 4)]))
    hairpin = Hairpin(descriptor='<', direction=Up)
    attach(hairpin, target[:3])
    hairpin = Hairpin(descriptor='>', direction=Down)
    attach(hairpin, target[2:])
    dynamic = Dynamic('ppp')
    attach(dynamic, target[-1])

    assert format(target) == stringtools.normalize(
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


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_08():

    string = r"\new Staff { c'4 ( \p \< d'4 e'4 f'4 ) \! }"
    parser = LilyPondParser()
    result = parser(string)
    assert format(result) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 \p \< (
            d'4
            e'4
            f'4 \! )
        }
        '''
        )
