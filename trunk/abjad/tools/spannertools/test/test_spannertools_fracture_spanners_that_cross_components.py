# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_fracture_spanners_that_cross_components_01():
    r'''Fracture all spanners to the left of the leftmost component in list;
        fracture all spanners to the right of the rightmost component in list.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff[:])
    spannertools.fracture_spanners_that_cross_components(staff[1:3])

    r'''
    \new Staff {
        c'8 [ ]
        d'8 [
        e'8 ]
        f'8 [ ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [ ]
            d'8 [
            e'8 ]
            f'8 [ ]
        }
        '''
        )


def test_spannertools_fracture_spanners_that_cross_components_02():
    r'''Fracture to the left of leftmost component;
        fracture to the right of rightmost component.'''

    staff = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(staff[:])
    spannertools.fracture_spanners_that_cross_components(staff[1:2])

    r'''
    \new Staff {
        c'8 [ ]
        d'8 [ ]
        e'8 [
        f'8 ]
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 [ ]
            d'8 [ ]
            e'8 [
            f'8 ]
        }
        '''
        )


def test_spannertools_fracture_spanners_that_cross_components_03():
    r'''Empty list raises no exception.
    '''

    result = spannertools.fracture_spanners_that_cross_components([])
    assert result == []


def test_spannertools_fracture_spanners_that_cross_components_04():
    r'''Fractures around components at only top level of list.
    '''

    staff = Staff(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.CrescendoSpanner(staff)
    spannertools.BeamSpanner(staff[:])

    r'''
    \new Staff {
        {
            c'8 [ \<
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ] \!
        }
    }
    '''

    spannertools.fracture_spanners_that_cross_components(staff[1:2])

    r'''
    \new Staff {
        {
            c'8 [ \<
            d'8 ]
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8 [
            a'8 ] \!
        }
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            {
                c'8 [ \<
                d'8 ]
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8 [
                a'8 ] \!
            }
        }
        '''
        )


def test_spannertools_fracture_spanners_that_cross_components_05():
    r'''Fractures around components at only top level of list.
    '''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.CrescendoSpanner(t)
    spannertools.BeamSpanner(t[:])
    spannertools.TrillSpanner(t.select_leaves())

    r'''
    \new Staff {
        {
            c'8 [ \< \startTrillSpan
            d'8
        }
        {
            e'8
            f'8
        }
        {
            g'8
            a'8 ] \! \stopTrillSpan
        }
    }
    '''

    spannertools.fracture_spanners_that_cross_components(t[1:2])

    r'''
    \new Staff {
        {
            c'8 [ \< \startTrillSpan
            d'8 ]
        }
        {
            e'8 [
            f'8 ]
        }
        {
            g'8 [
            a'8 ] \! \stopTrillSpan
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            {
                c'8 [ \< \startTrillSpan
                d'8 ]
            }
            {
                e'8 [
                f'8 ]
            }
            {
                g'8 [
                a'8 ] \! \stopTrillSpan
            }
        }
        '''
        )
