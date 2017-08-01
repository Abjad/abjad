# -*- coding: utf-8 -*-
import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_01():

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 5, [(1, 4)]))
    hairpin = abjad.Hairpin(descriptor='<')
    abjad.attach(hairpin, target[:3])
    hairpin = abjad.Hairpin(descriptor='>')
    abjad.attach(hairpin, target[2:])
    dynamic = abjad.Dynamic('ppp')
    abjad.attach(dynamic, target[-1])

    assert format(target) == abjad.String.normalize(
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

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_02():

    maker = abjad.NoteMaker()
    target = abjad.Container(maker([0] * 4, [(1, 4)]))
    hairpin = abjad.Hairpin(descriptor='<')
    abjad.attach(hairpin, target[0:2])
    hairpin = abjad.Hairpin(descriptor='<')
    abjad.attach(hairpin, target[1:3])
    hairpin = abjad.Hairpin(descriptor='<')
    abjad.attach(hairpin, target[2:])

    assert format(target) == abjad.String.normalize(
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
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_03():
    r'''Dynamics can terminate hairpins.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 3, [(1, 4)]))
    hairpin = abjad.Hairpin(descriptor='<')
    abjad.attach(hairpin, target[0:2])
    hairpin = abjad.Hairpin(descriptor='>')
    abjad.attach(hairpin, target[1:])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, target[1])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, target[-1])

    assert format(target) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4 \<
            c'4 \p \>
            c'4 \f
        }
        '''
        )

    string = r"\new Staff \relative c' { c \< c \p \> c \f }"
    parser = abjad.lilypondparsertools.LilyPondParser()
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
    result = abjad.lilypondparsertools.LilyPondParser()(string)


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_06():
    r'''No double dynamic spans permitted.
    '''

    string = r'{ c \< \> c c c \! }'
    assert pytest.raises(Exception, 'LilyPondParser()(string)')


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_07():
    r'''With direction.
    '''

    maker = abjad.NoteMaker()
    target = abjad.Staff(maker([0] * 5, [(1, 4)]))
    hairpin = abjad.Hairpin(descriptor='<', direction=Up)
    abjad.attach(hairpin, target[:3])
    hairpin = abjad.Hairpin(descriptor='>', direction=Down)
    abjad.attach(hairpin, target[2:])
    dynamic = abjad.Dynamic('ppp')
    abjad.attach(dynamic, target[-1])

    assert format(target) == abjad.String.normalize(
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

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result


def test_lilypondparsertools_LilyPondParser__spanners__Hairpin_08():

    string = r"\new Staff { c'4 ( \p \< d'4 e'4 f'4 ) \! }"
    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(result) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4 \p \< (
            d'4
            e'4
            f'4 \! )
        }
        '''
        )
