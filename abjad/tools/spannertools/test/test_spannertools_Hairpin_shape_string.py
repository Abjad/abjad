# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin_shape_string_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, staff[:])

    assert hairpin.shape_string == '<'
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            d'8
            e'8
            f'8 \!
        }
        '''
        )

    hairpin.shape_string = '>'

    r'''
    \new Staff {
        c'8 \>
        d'8
        e'8
        f'8 \!
    }
    '''

    assert hairpin.shape_string == '>'
    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \>
            d'8
            e'8
            f'8 \!
        }
        '''
        )
