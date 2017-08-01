# -*- coding: utf-8 -*-
import abjad


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_01():
    r'''Span isolated_nib_direction note when isolated_nib_direction is set to
    true.
    '''

    container = abjad.Container("c'8")
    beam = abjad.DuratedComplexBeam(isolated_nib_direction=True)
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            c'8 [ ]
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_02():
    r'''Do not span isolated_nib_direction note when isolated_nib_direction
    is set to false.
    '''

    container = abjad.Container("c'8")
    beam = abjad.DuratedComplexBeam(isolated_nib_direction=False)
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            c'8
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_03():
    r'''Ignore isolated_nib_direction when spanner spans more than one leaf.
    '''

    container = abjad.Container("c'8 d'8")
    beam = abjad.DuratedComplexBeam(isolated_nib_direction=False)
    abjad.attach(beam, container[:])

    assert format(container) == abjad.String.normalize(
        r'''
        {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #1
            c'8 [
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #0
            d'8 ]
        }
        '''
        )

    assert abjad.inspect(container).is_well_formed()
