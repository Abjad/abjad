# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Crescendo___init___01():
    r'''Initialize empty crescendo spanner.
    '''

    crescendo = Crescendo()
    assert isinstance(crescendo, Crescendo)


def test_spannertools_Crescendo___init___02():

    staff = Staff("c'8 d'8 e'8 f'8 g'2")
    crescendo = Crescendo()
    attach(crescendo, staff[:4])

    assert format(staff) == stringtools.normalize(
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
