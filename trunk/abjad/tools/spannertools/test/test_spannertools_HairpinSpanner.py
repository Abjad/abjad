# -*- encoding: utf-8 -*-
import py.test
from abjad import *
from abjad.tools.wellformednesstools import IntermarkedHairpinCheck
from abjad.tools.wellformednesstools import ShortHairpinCheck


def test_spannertools_HairpinSpanner_01():
    r'''Hairpins span adjacent leaves.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:4])

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


def test_spannertools_HairpinSpanner_02():
    r'''Hairpins spanning a single leaf are allowed but not well-formed.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[0:1])
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


def test_spannertools_HairpinSpanner_03():
    r'''Hairpins and dynamics apply separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:4])
    contexttools.DynamicMark('p')(staff[0])
    contexttools.DynamicMark('f')(staff[3])

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


def test_spannertools_HairpinSpanner_04():
    r'''Internal marks raise well-formedness error.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:4])
    statement = "contexttools.DynamicMark('p')(staff[2])"
    assert py.test.raises(WellFormednessError, statement)


def test_spannertools_HairpinSpanner_05():
    r'''Apply back-to-back hairpins separately.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    contexttools.DynamicMark('p')(staff[0])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[0:3])
    contexttools.DynamicMark('f')(staff[2])
    decrescendo = spannertools.DecrescendoSpanner()
    decrescendo.attach(staff[2:5])
    contexttools.DynamicMark('p')(staff[4])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[4:7])
    contexttools.DynamicMark('f')(staff[6])

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


def test_spannertools_HairpinSpanner_06():
    r'''Hairpins format rests.
    '''

    staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    crescendo = spannertools.CrescendoSpanner()
    crescendo.attach(staff[:])

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


def test_spannertools_HairpinSpanner_07():
    r'''Trimmed hairpins with dynamic marks behave as expected.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    rest = Rest(staff[0])
    staff[0] = rest
    rest = Rest(staff[-1])
    staff[-1] = rest
    hairpin = spannertools.HairpinSpanner(
        descriptor='p < f', 
        include_rests=False,
        )
    hairpin.attach(staff.select_leaves())

    spanner_classes = spannertools.HairpinSpanner
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
