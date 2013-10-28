# -*- encoding: utf-8 -*-
import py.test
from abjad import *


def test_mutationtools_ScoreMutationAgent_swap_01():
    r'''Move parentage, children and spanners from multiple containers 
    to empty tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 8), [])
    mutate(voice[:2]).swap(tuplet)

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'8 [
                d'8
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_swap_02():
    r'''Move parentage, children and spanners from container to empty voice.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    voice.name = 'foo'
    glissando = spannertools.GlissandoSpanner()
    glissando.attach(voice[:])
    beam = spannertools.BeamSpanner()
    attach(beam, voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \context Voice = "foo" {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    new_voice = Voice()
    new_voice.name = 'foo'
    mutate(voice[1:2]).swap(new_voice)

    assert testtools.compare(
        voice,
        r'''
        \context Voice = "foo" {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \context Voice = "foo" {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_swap_03():
    r'''Move parentage, children and spanners from container to empty tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    glissando = spannertools.GlissandoSpanner()
    glissando.attach(voice[:])
    beam = spannertools.BeamSpanner()
    attach(beam, voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 16), [])
    mutate(voice[1:2]).swap(tuplet)


    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \tweak #'text #tuplet-number::calc-fraction-text
            \times 3/4 {
                e'8 \glissando
                f'8 \glissando
            }
            {
                g'8 \glissando
                a'8 ]
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_mutationtools_ScoreMutationAgent_swap_04():
    r'''Trying to move parentage, children and spanners to noncontainer 
    raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    note = Note("c'4")
    assert py.test.raises(
        Exception, 
        'mutate(voice[1:2]).swap(note)',
        )


def test_mutationtools_ScoreMutationAgent_swap_05():
    r'''Trying to move parentage, children and spanners from 
    nonempty container to nonempty container raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice[:])

    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert py.test.raises(
        Exception, 
        'mutate(voice[1:2]).swap(tuplet)',
        )


def test_mutationtools_ScoreMutationAgent_swap_06():
    r'''Trying to move parentage, children and spanners from components 
    that are not parent-contiguous raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    beam = spannertools.BeamSpanner()
    attach(beam, voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                c'8 [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8 ]
            }
        }
        '''
        )

    tuplet = tuplettools.FixedDurationTuplet(Duration(3, 8), [])
    assert py.test.raises(
        Exception, 
        'mutate([voice[0], voice[2]]).swap(tuplet)',
        )


def test_mutationtools_ScoreMutationAgent_swap_07():
    r'''Move parentage, children and spanners from one measure to another.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

    assert testtools.compare(
        measure,
        r'''
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    new_measure = Measure((4, 8), [])
    mutate(measure).swap(new_measure)

    assert testtools.compare(
        new_measure,
        r'''
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    assert inspect(new_measure).is_well_formed()
