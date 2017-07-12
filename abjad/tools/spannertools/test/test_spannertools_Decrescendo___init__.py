# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Decrescendo___init___01():
    r'''Initialize empty decrescendo spanner.
    '''

    decrescendo = abjad.Decrescendo()
    assert isinstance(decrescendo, abjad.Decrescendo)


def test_spannertools_Decrescendo___init___02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8 g'2")
    decrescendo = abjad.Decrescendo()
    abjad.attach(decrescendo, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \>
            d'8
            e'8
            f'8 \!
            g'2
        }
        '''
        )
