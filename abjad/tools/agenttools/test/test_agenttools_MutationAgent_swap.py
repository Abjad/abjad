# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_MutationAgent_swap_01():
    r'''Moves parentage, children and spanners from multiple containers
    to empty tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
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

    tuplet = scoretools.FixedDurationTuplet(Duration(3, 8), [])
    mutate(voice[:2]).swap(tuplet)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            \tweak text #tuplet-number::calc-fraction-text
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_swap_02():
    r'''Moves parentage, children and spanners from container to empty voice.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    voice.name = 'foo'
    glissando = spannertools.Glissando()
    attach(glissando, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
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

    assert format(voice) == stringtools.normalize(
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_swap_03():
    r'''Moves parentage, children and spanners from container to empty tuplet.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    glissando = spannertools.Glissando()
    attach(glissando, leaves)
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
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

    tuplet = scoretools.FixedDurationTuplet(Duration(3, 16), [])
    mutate(voice[1:2]).swap(tuplet)


    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            {
                c'8 [ \glissando
                d'8 \glissando
            }
            \tweak text #tuplet-number::calc-fraction-text
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

    assert inspect_(voice).is_well_formed()


def test_agenttools_MutationAgent_swap_04():
    r'''Trying to move parentage, children and spanners to noncontainer
    raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    note = Note("c'4")
    assert pytest.raises(Exception, 'mutate(voice[1:2]).swap(note)')


def test_agenttools_MutationAgent_swap_05():
    r'''Trying to move parentage, children and spanners from
    nonempty container to nonempty container raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    assert pytest.raises(Exception, 'mutate(voice[1:2]).swap(tuplet)')


def test_agenttools_MutationAgent_swap_06():
    r'''Trying to move parentage, children and spanners from components
    that are not parent-contiguous raises exception.
    '''

    voice = Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
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

    tuplet = scoretools.FixedDurationTuplet(Duration(3, 8), [])
    statement = 'mutate([voice[0], voice[2]]).swap(tuplet)'
    assert pytest.raises(Exception, statement)


def test_agenttools_MutationAgent_swap_07():
    r'''Moves parentage, children and spanners from one measure to another.
    '''

    measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

    assert format(measure) == stringtools.normalize(
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

    assert format(new_measure) == stringtools.normalize(
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

    assert inspect_(new_measure).is_well_formed()
