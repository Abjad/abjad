# -*- encoding: utf-8 -*-
from abjad import *


def test_containertools_repeat_contents_of_container_01():
    r'''Multiply notes in voice.
    '''

    voice = Voice("c'8 d'8")
    spannertools.BeamSpanner(voice[:])
    containertools.repeat_contents_of_container(voice, total=3)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
        c'8 [
        d'8 ]
        c'8 [
        d'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            c'8 [
            d'8 ]
            c'8 [
            d'8 ]
        }
        '''
        )


def test_containertools_repeat_contents_of_container_02():
    r'''Multiplication by one leaves contents unchanged.
    '''

    voice = Voice("c'8 d'8")
    spannertools.BeamSpanner(voice[:])
    containertools.repeat_contents_of_container(voice, total=1)

    r'''
    \new Voice {
        c'8 [
        d'8 ]
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8 [
            d'8 ]
        }
        '''
        )


def test_containertools_repeat_contents_of_container_03():
    r'''Multiplication by zero empties container.
    '''

    voice = Voice("c'8 d'8")
    spannertools.BeamSpanner(voice[:])
    containertools.repeat_contents_of_container(voice, total=0)

    r'''
    \new Voice {
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
        }
        '''
        )
