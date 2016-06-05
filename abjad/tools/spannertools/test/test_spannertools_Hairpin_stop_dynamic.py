# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_stop_dynamic_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='p < f')
    attach(hairpin, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \f
        }
        '''
        )

    assert hairpin.stop_dynamic == Dynamic('f')


def test_spannertools_Hairpin_stop_dynamic_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='p < mf')
    attach(hairpin, staff[:])

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \mf
        }
        '''
        )

    assert hairpin.stop_dynamic == Dynamic('mf')
