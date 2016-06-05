# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Decrescendo___init___01():
    r'''Initialize empty decrescendo spanner.
    '''

    decrescendo = Decrescendo()
    assert isinstance(decrescendo, Decrescendo)


def test_spannertools_Decrescendo___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    decrescendo = Decrescendo()
    attach(decrescendo, staff[:4])

    assert format(staff) == stringtools.normalize(
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
