# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin_stop_dynamic_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = abjad.Hairpin(descriptor='p < f')
    abjad.attach(hairpin, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \f
        }
        '''
        )

    assert hairpin.stop_dynamic == abjad.Dynamic('f')


def test_spannertools_Hairpin_stop_dynamic_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = abjad.Hairpin(descriptor='p < mf')
    abjad.attach(hairpin, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \< \p
            d'8
            e'8
            f'8 \mf
        }
        '''
        )

    assert hairpin.stop_dynamic == abjad.Dynamic('mf')
