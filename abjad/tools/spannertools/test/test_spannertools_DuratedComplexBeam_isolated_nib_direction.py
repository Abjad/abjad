# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_01():
    r'''Span isolated_nib_direction note when isolated_nib_direction is set to
    true.
    '''

    container = Container("c'8")
    beam = spannertools.DuratedComplexBeam(isolated_nib_direction=True)
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            \set stemLeftBeamCount = #1
            \set stemRightBeamCount = #1
            c'8 [ ]
        }
        '''
        )

    assert inspect_(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_02():
    r'''Do not span isolated_nib_direction note when isolated_nib_direction
    is set to false.
    '''

    container = Container("c'8")
    beam = spannertools.DuratedComplexBeam(isolated_nib_direction=False)
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8
        }
        '''
        )

    assert inspect_(container).is_well_formed()


def test_spannertools_DuratedComplexBeam_isolated_nib_direction_03():
    r'''Ignore isolated_nib_direction when spanner spans more than one leaf.
    '''

    container = Container("c'8 d'8")
    beam = spannertools.DuratedComplexBeam(isolated_nib_direction=False)
    attach(beam, container[:])

    assert format(container) == stringtools.normalize(
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

    assert inspect_(container).is_well_formed()