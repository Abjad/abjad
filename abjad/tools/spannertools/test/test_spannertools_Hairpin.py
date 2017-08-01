# -*- coding: utf-8 -*-
import abjad
import pytest


def test_spannertools_Hairpin_01():
    r'''Hairpins span adjacent leaves.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[:4])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_02():
    r'''Hairpins and dynamics apply separately.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[:4])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, staff[0])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, staff[3])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \p \<
            cs'8
            d'8
            ef'8 \f
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_03():

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[:4])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, staff[2])

    assert not abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_04():
    r'''Apply back-to-back hairpins separately.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, staff[0])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[0:3])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, staff[2])
    decrescendo = abjad.Hairpin('>')
    abjad.attach(decrescendo, staff[2:5])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, staff[4])
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, staff[4:7])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, staff[6])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 \p \<
            cs'8
            d'8 \f \>
            ef'8
            e'8 \p \<
            f'8
            fs'8 \f
            g'8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_05():
    r'''Hairpins format rests.
    '''

    staff = abjad.Staff(abjad.Rest((1, 8)) * 4 + [abjad.Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = abjad.Hairpin('<', include_rests=True)
    abjad.attach(crescendo, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            r8 \<
            r8
            r8
            r8
            e'8
            f'8
            fs'8
            g'8 \!
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_06():
    r'''Trimmed hairpins with dynamics behave as expected.
    '''

    staff = abjad.Staff([abjad.Note(n, (1, 8)) for n in range(8)])
    rest = abjad.Rest(staff[0])
    staff[0] = rest
    rest = abjad.Rest(staff[-1])
    staff[-1] = rest
    hairpin = abjad.Hairpin(
        descriptor='p < f',
        include_rests=False,
        )
    abjad.attach(hairpin, staff[:])

    prototype = abjad.Hairpin
    spanner = abjad.inspect(staff[0]).get_spanner(prototype=prototype)
    assert len(spanner.components) == len(staff)

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            r8
            cs'8 \< \p
            d'8
            ef'8
            e'8
            f'8
            fs'8 \f
            r8
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_spannertools_Hairpin_07():
    
    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.attach(abjad.Dynamic('p'), staff[0])
    abjad.attach(abjad.Hairpin('<'), staff[:])
    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'4 \p \<
            d'4
            e'4
            f'4 \!
        }
        '''
        )
