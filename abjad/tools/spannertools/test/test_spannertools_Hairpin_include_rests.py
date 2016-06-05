# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_include_rests_01():
    r'''Hairpin spanner avoids rests.
    '''

    staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = Crescendo(include_rests=False)
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_include_rests_02():
    r'''Hairpin spanner avoids rests.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
    crescendo = Crescendo(include_rests=False)
    attach(crescendo, staff[:])


    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()
