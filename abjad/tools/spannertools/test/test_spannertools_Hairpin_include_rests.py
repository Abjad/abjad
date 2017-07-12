# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin_include_rests_01():
    r'''Hairpin spanner avoids rests.
    '''

    staff = abjad.Staff(abjad.Rest((1, 8)) * 4 + [abjad.Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = abjad.Crescendo(include_rests=False)
    abjad.attach(crescendo, staff[:])

    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_include_rests_02():
    r'''Hairpin spanner avoids rests.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(4)] + abjad.Rest((1, 8)) * 4)
    crescendo = abjad.Crescendo(include_rests=False)
    abjad.attach(crescendo, staff[:])


    assert format(staff) == abjad.String.normalize(
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

    assert abjad.inspect(staff).is_well_formed()
