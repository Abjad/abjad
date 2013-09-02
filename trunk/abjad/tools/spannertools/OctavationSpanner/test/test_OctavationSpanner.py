# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.wellformednesstools import OverlappingOctavationCheck


def test_OctavationSpanner_01():
    r'''Octavation has default start set to 1 and stop set to 0.
    '''

    staff = Staff(notetools.make_repeated_notes(4))
    o = spannertools.OctavationSpanner(staff[:])

    assert o.start == 1
    assert o.stop == 0

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            c'8
            c'8
            c'8
            \ottava #0
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_OctavationSpanner_02():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.OctavationSpanner(staff[:4], 1)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            cs'8
            d'8
            ef'8
            \ottava #0
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_OctavationSpanner_03():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.OctavationSpanner(staff[:4], 1, 2)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            cs'8
            d'8
            ef'8
            \ottava #2
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_OctavationSpanner_04():
    r'''One-note octavation changes are allowed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.OctavationSpanner(staff[0], 1)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            \ottava #0
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_OctavationSpanner_05():
    r'''Adjacent one-note octavation changes are allowed;
    TODO: check for back-to-back set-octavation at format-
    time and compress to a single set-octavation.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.OctavationSpanner(staff[0], 1)
    spannertools.OctavationSpanner(staff[1], 2)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            \ottava #0
            \ottava #2
            cs'8
            \ottava #0
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect(staff).is_well_formed()


def test_OctavationSpanner_06():
    r'''Overlapping octavation spanners are allowed but not well-formed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.OctavationSpanner(staff[:4], 1)
    spannertools.OctavationSpanner(staff[2:6], 2)
    checker = OverlappingOctavationCheck()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \ottava #1
            c'8
            cs'8
            \ottava #2
            d'8
            ef'8
            \ottava #0
            e'8
            f'8
            \ottava #0
            fs'8
            g'8
        }
        '''
        )

    assert not checker.check(staff)
