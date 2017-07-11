# -*- coding: utf-8 -*-
import abjad
from abjad import *


def test_spannertools_Hairpin_shape_string_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='<')
    attach(hairpin, staff[:])

    assert format(staff) == String.normalize(
        r'''
        \new Staff {
            c'8 \<
            d'8
            e'8
            f'8 \!
        }
        '''
        )

    assert hairpin.shape_string == '<'


def test_spannertools_Hairpin_shape_string_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = Hairpin(descriptor='>')
    attach(hairpin, staff[:])

    assert format(staff) == String.normalize(
        r'''
        \new Staff {
            c'8 \>
            d'8
            e'8
            f'8 \!
        }
        '''
        )

    assert hairpin.shape_string == '>'
