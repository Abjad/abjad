# -*- encoding: utf-8 -*-
from abjad import *


def test_MutationInterface_split_in_halves_01():

    staff = Staff("c'8 ( d'8 e'8 f'8 )")
    mutate(staff[0]).split_in_halves(n=4)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'32 (
            c'32
            c'32
            c'32
            d'8
            e'8
            f'8 )
        }
        '''
        )

    assert select(staff).is_well_formed()
