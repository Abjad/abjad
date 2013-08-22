# -*- encoding: utf-8 -*-
from abjad import *


# TODO: move to test_Measure___init__.py

def test_Measure_in_place_apply_01():

    voice = Voice([Note(n, (1, 8)) for n in range(8)])
    leaves_before = voice.select_leaves()
    Measure((4, 8), voice[0:4])
    leaves_after = voice.select_leaves()

    r'''
    \new Voice {
        {
            \time 4/8
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            {
                \time 4/8
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )


def test_Measure_in_place_apply_02():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    leaves_before = staff.select_leaves()
    Measure((4, 8), staff[0:4])
    leaves_after = staff.select_leaves()

    r'''
    \new Staff {
        {
            \time 4/8
            c'8
            cs'8
            d'8
            ef'8
        }
        e'8
        f'8
        fs'8
        g'8
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 4/8
                c'8
                cs'8
                d'8
                ef'8
            }
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )


def test_Measure_in_place_apply_03():

    staff = Staff([Note(n, (1, 1)) for n in range(4)])
    leaves_before = staff.select_leaves()
    Measure((1, 1), staff[0:1])
    leaves_after = staff.select_leaves()

    r'''
    \new Staff {
        {
            \time 1/1
            c'1
        }
        cs'1
        d'1
        ef'1
    }
    '''

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/1
                c'1
            }
            cs'1
            d'1
            ef'1
        }
        '''
        )


def test_Measure_in_place_apply_04():

    staff = Staff([Note(n, (1, 1)) for n in range(4)])
    Measure((1, 1), staff[:1])
    Measure((1, 1), staff[1:2])
    Measure((1, 1), staff[2:3])
    Measure((1, 1), staff[3:])
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 1/1
            c'1
        }
        {
            \time 1/1
            cs'1
        }
        {
            \time 1/1
            d'1
        }
        {
            \time 1/1
            ef'1
        }
    }
    '''

    assert inspect(staff).is_well_formed()
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 1/1
                c'1
            }
            {
                \time 1/1
                cs'1
            }
            {
                \time 1/1
                d'1
            }
            {
                \time 1/1
                ef'1
            }
        }
        '''
        )
