# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_HairpinSpanner_stop_dynamic_string_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = HairpinSpanner(descriptor='p < f')
    attach(hairpin, staff[:])

    assert hairpin.stop_dynamic_string == 'f'
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \f
        }
        '''
        )

    hairpin.stop_dynamic_string = 'mf'

    assert hairpin.stop_dynamic_string == 'mf'
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \mf
        }
        '''
        )
