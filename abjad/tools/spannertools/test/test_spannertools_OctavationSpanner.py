# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_OctavationSpanner_01():
    r'''Octavation has default start set to 1 and stop set to 0.
    '''

    staff = Staff(scoretools.make_repeated_notes(4))
    spanner =  spannertools.OctavationSpanner()
    attach(spanner, staff[:])

    assert spanner.start == 1
    assert spanner.stop == 0

    assert systemtools.TestManager.compare(
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


def test_spannertools_OctavationSpanner_02():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spanner = spannertools.OctavationSpanner(start=1)
    attach(spanner, staff[:4])

    assert systemtools.TestManager.compare(
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


def test_spannertools_OctavationSpanner_03():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spanner = spannertools.OctavationSpanner(start=1, stop=2)
    attach(spanner, staff[:4])

    assert systemtools.TestManager.compare(
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


def test_spannertools_OctavationSpanner_04():
    r'''One-note octavation changes are allowed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spanner = spannertools.OctavationSpanner(start=1)
    attach(spanner, staff[0])

    assert systemtools.TestManager.compare(
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


def test_spannertools_OctavationSpanner_05():
    r'''Adjacent one-note octavation changes are allowed;
    TODO: check for back-to-back set-octavation at format-
    time and compress to a single set-octavation.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spanner = spannertools.OctavationSpanner(start=1)
    attach(spanner, staff[0])
    spanner = spannertools.OctavationSpanner(start=2)
    attach(spanner, staff[1])

    assert systemtools.TestManager.compare(
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


def test_spannertools_OctavationSpanner_06():
    r'''Overlapping octavation spanners are allowed but not well-formed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spanner = spannertools.OctavationSpanner(start=1)
    attach(spanner, staff[:4])
    spanner = spannertools.OctavationSpanner(start=2)
    attach(spanner, staff[2:6])

    assert systemtools.TestManager.compare(
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

    assert not inspect(staff).is_well_formed()
