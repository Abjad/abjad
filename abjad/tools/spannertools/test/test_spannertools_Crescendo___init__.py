# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Crescendo___init___01():
    r'''Initialize empty crescendo spanner.
    '''

    crescendo = abjad.Crescendo()
    assert isinstance(crescendo, abjad.Crescendo)


def test_spannertools_Crescendo___init___02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    crescendo = abjad.Crescendo()
    abjad.attach(crescendo, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \<
            d'8
            e'8
            f'8 \!
            g'2
        }
        '''
        )
