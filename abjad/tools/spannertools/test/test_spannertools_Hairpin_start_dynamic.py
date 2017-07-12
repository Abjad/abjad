# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin_start_dynamic_01():

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

    assert hairpin.start_dynamic == abjad.Dynamic('p')


def test_spannertools_Hairpin_start_dynamic_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    hairpin = abjad.Hairpin(descriptor='mf < f')
    abjad.attach(hairpin, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \< \mf
            d'8
            e'8
            f'8 \f
        }
        '''
        )

    assert hairpin.start_dynamic == abjad.Dynamic('mf')
