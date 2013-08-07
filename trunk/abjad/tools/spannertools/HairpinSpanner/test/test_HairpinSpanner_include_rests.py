# -*- encoding: utf-8 -*-
from abjad import *


def test_HairpinSpanner_include_rests_01():
    r'''Hairpin spanner avoids rests.
    '''

    staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    spannertools.CrescendoSpanner(staff[:], include_rests=False)

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
        e'8 \<
        f'8
        fs'8
        g'8 \!
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            r8
            r8
            r8
            r8
            e'8 \<
            f'8
            fs'8
            g'8 \!
        }
        '''
        )


def test_HairpinSpanner_include_rests_02():
    r'''Hairpin spanner avoids rests.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
    spannertools.CrescendoSpanner(staff[:], include_rests=False)


    r'''
    \new Staff {
        c'8 \<
        cs'8
        d'8
        ef'8 \!
        r8
        r8
        r8
        r8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            r8
            r8
            r8
            r8
        }
        '''
        )
