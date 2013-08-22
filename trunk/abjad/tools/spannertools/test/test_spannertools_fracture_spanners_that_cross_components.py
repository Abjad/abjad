# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_fracture_spanners_that_cross_components_01():
    r'''Fracture all spanners to the left of the leftmost component in list;
    fracture all spanners to the right of the rightmost component in list.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(container[:])
    spannertools.fracture_spanners_that_cross_components(container[1:3])

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ]
            d'8 [
            e'8 ]
            f'8 [ ]
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_spannertools_fracture_spanners_that_cross_components_02():
    r'''Fracture to the left of leftmost component;
    fracture to the right of rightmost component.
    '''

    container = Container("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(container[:])
    spannertools.fracture_spanners_that_cross_components(container[1:2])

    assert testtools.compare(
        container,
        r'''
        {
            c'8 [ ]
            d'8 [ ]
            e'8 [
            f'8 ]
        }
        '''
        )

    assert inspect(container).is_well_formed()


def test_spannertools_fracture_spanners_that_cross_components_03():
    r'''Empty list raises no exception.
    '''

    result = spannertools.fracture_spanners_that_cross_components([])
    assert result == []


def test_spannertools_fracture_spanners_that_cross_components_04():
    r'''Fractures around components at only top level of list.
    '''

    container = Container(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
    container)
    spannertools.CrescendoSpanner(container)
    spannertools.BeamSpanner(container[:])

    assert testtools.compare(
        container,
        r'''
        {
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
        )

    spannertools.fracture_spanners_that_cross_components(container[1:2])

    assert testtools.compare(
        container,
        r'''
        {
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

    assert inspect(container).is_well_formed()


def test_spannertools_fracture_spanners_that_cross_components_05():
    r'''Fractures around components at only top level of list.
    '''

    container = Container(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
    container)
    spannertools.CrescendoSpanner(container)
    spannertools.BeamSpanner(container[:])
    spannertools.TrillSpanner(container.select_leaves())

    assert testtools.compare(
        container,
        r'''
        {
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
        )

    spannertools.fracture_spanners_that_cross_components(container[1:2])

    assert testtools.compare(
        container,
        r'''
        {
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

    assert inspect(container).is_well_formed()
