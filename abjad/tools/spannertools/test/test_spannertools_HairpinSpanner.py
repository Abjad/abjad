# -*- encoding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.wellformednesstools import IntermarkedHairpinCheck
from abjad.tools.wellformednesstools import ShortHairpinCheck


def test_HairpinSpanner_01():
    r'''Hairpins span adjacent leaves.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[:4])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_HairpinSpanner_02():
    r'''Hairpins spanning a single leaf are allowed but not well-formed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[0:1])
    checker = ShortHairpinCheck()

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \< \!
            cs'8
            d'8
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert not checker.check(staff)


def test_HairpinSpanner_03():
    r'''Hairpins and dynamics apply separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[:4])
    dynamic = DynamicMark('p')
    attach(dynamic, staff[0])
    dynamic = DynamicMark('f')
    attach(dynamic, staff[3])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_HairpinSpanner_04():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[:4])
    dynamic = DynamicMark('p')
    attach(dynamic, staff[2])

    assert not inspect(staff).is_well_formed()


def test_HairpinSpanner_05():
    r'''Apply back-to-back hairpins separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    dynamic = DynamicMark('p')
    attach(dynamic, staff[0])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[0:3])
    dynamic = DynamicMark('f')
    attach(dynamic, staff[2])
    decrescendo = DecrescendoSpanner()
    attach(decrescendo, staff[2:5])
    dynamic = DynamicMark('p')
    attach(dynamic, staff[4])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[4:7])
    dynamic = DynamicMark('f')
    attach(dynamic, staff[6])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_HairpinSpanner_06():
    r'''Hairpins format rests.
    '''

    staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = CrescendoSpanner()
    attach(crescendo, staff[:])

    assert testtools.compare(
        staff,
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

    assert inspect(staff).is_well_formed()


def test_HairpinSpanner_07():
    r'''Trimmed hairpins with dynamic marks behave as expected.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    rest = Rest(staff[0])
    staff[0] = rest
    rest = Rest(staff[-1])
    staff[-1] = rest
    hairpin = HairpinSpanner(
        descriptor='p < f', 
        include_rests=False,
        )
    attach(hairpin, staff.select_leaves())

    spanner_classes = HairpinSpanner
    spanner = inspect(staff[0]).get_spanner(spanner_classes=spanner_classes)
    assert len(spanner.components) == len(staff)

    assert testtools.compare(
        staff,
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

    checker = IntermarkedHairpinCheck()
    assert checker.check(staff)
