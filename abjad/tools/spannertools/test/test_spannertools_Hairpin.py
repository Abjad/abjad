# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_spannertools_Hairpin_01():
    r'''Hairpins span adjacent leaves.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = Crescendo()
    attach(crescendo, staff[:4])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_02():
    r'''Hairpins and dynamics apply separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = Crescendo()
    attach(crescendo, staff[:4])
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])
    dynamic = Dynamic('f')
    attach(dynamic, staff[3])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_03():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = Crescendo()
    attach(crescendo, staff[:4])
    dynamic = Dynamic('p')
    attach(dynamic, staff[2])

    assert not inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_04():
    r'''Apply back-to-back hairpins separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    dynamic = Dynamic('p')
    attach(dynamic, staff[0])
    crescendo = Crescendo()
    attach(crescendo, staff[0:3])
    dynamic = Dynamic('f')
    attach(dynamic, staff[2])
    decrescendo = Decrescendo()
    attach(decrescendo, staff[2:5])
    dynamic = Dynamic('p')
    attach(dynamic, staff[4])
    crescendo = Crescendo()
    attach(crescendo, staff[4:7])
    dynamic = Dynamic('f')
    attach(dynamic, staff[6])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_05():
    r'''Hairpins format rests.
    '''

    staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = Crescendo(include_rests=True)
    attach(crescendo, staff[:])

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_06():
    r'''Trimmed hairpins with dynamics behave as expected.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    rest = Rest(staff[0])
    staff[0] = rest
    rest = Rest(staff[-1])
    staff[-1] = rest
    hairpin = Hairpin(
        descriptor='p < f',
        include_rests=False,
        )
    attach(hairpin, staff[:])

    prototype = Hairpin
    spanner = inspect_(staff[0]).get_spanner(prototype=prototype)
    assert len(spanner.components) == len(staff)

    assert format(staff) == stringtools.normalize(
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

    assert inspect_(staff).is_well_formed()


def test_spannertools_Hairpin_07():
    
    staff = Staff("c'4 d'4 e'4 f'4")
    attach(Dynamic('p'), staff[0])
    attach(Hairpin('<'), staff[:])
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'4 \p \<
            d'4
            e'4
            f'4 \!
        }
        '''
        )