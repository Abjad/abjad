# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin_direction_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = abjad.Hairpin(descriptor='p < f', direction=Down)
    abjad.attach(hairpin, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 _ \< _ \p
            d'8
            e'8
            f'8 _ \f
        }
        '''
        )
