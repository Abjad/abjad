# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_start_dynamic_string_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='p < f')
    attach(hairpin, staff[:])

    assert systemtools.TestManager.compare(
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

    assert hairpin.start_dynamic_string == 'p'


def test_foo_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='mf < f')
    attach(hairpin, staff[:])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \< \mf
            d'8
            e'8
            f'8 \f
        }
        '''
        )

    assert hairpin.start_dynamic_string == 'mf'
