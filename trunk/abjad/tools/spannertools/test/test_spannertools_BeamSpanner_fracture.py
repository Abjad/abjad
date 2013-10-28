# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_BeamSpanner_fracture_01():
    r'''This test shows that fracturing beyond the first leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:4])
    beam.fracture(0, direction=Left)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:4])
    beam.fracture(1, direction=Left)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
            d'8 [
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_03():
    r'''This test shows that fracurting beyond the last leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:4])
    beam.fracture(-1, direction=Right)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_04():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:4])
    beam.fracture(1, direction=Right)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_05():
    r'''Fracture both sides of leaf.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:5])
    beam.fracture(2, direction=None)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8 ]
            d'8 [ ]
            ef'8 [
            e'8 ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_06():
    r'''Fracture both sides of first leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:5])
    beam.fracture(0, direction=None)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
            cs'8 [
            d'8
            ef'8
            e'8 ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_07():
    r'''Fracture both sides of last leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:5])
    beam.fracture(4, direction=None)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            e'8 [ ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_spannertools_BeamSpanner_fracture_08():
    r'''Fracture both sides of leaf with negative index.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = spannertools.BeamSpanner()
    attach(beam, staff[:5])
    beam.fracture(-1, direction=None)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            e'8 [ ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()
