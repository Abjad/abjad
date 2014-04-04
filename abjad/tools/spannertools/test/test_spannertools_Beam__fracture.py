# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Beam__fracture_01():
    r'''This test shows that fracturing beyond the first leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = Beam()
    attach(beam, staff[:4])
    beam._fracture(0, direction=Left)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = Beam()
    attach(beam, staff[:4])
    beam._fracture(1, direction=Left)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
            d'8 [
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_03():
    r'''This test shows that fracurting beyond the last leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = Beam()
    attach(beam, staff[:4])
    beam._fracture(-1, direction=Right)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_04():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    beam = Beam()
    attach(beam, staff[:4])
    beam._fracture(1, direction=Right)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            d'8 ]
            e'8 [
            f'8 ]
            g'8
            a'8
            b'8
            c''8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_05():
    r'''Fracture both sides of leaf.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = Beam()
    attach(beam, staff[:5])
    beam._fracture(2, direction=None)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8 ]
            d'8 [ ]
            ef'8 [
            e'8 ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_06():
    r'''Fracture both sides of first leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = Beam()
    attach(beam, staff[:5])
    beam._fracture(0, direction=None)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [ ]
            cs'8 [
            d'8
            ef'8
            e'8 ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_07():
    r'''Fracture both sides of last leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = Beam()
    attach(beam, staff[:5])
    beam._fracture(4, direction=None)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            e'8 [ ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_08():
    r'''Fracture both sides of leaf with negative index.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beam = Beam()
    attach(beam, staff[:5])
    beam._fracture(-1, direction=None)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 [
            cs'8
            d'8
            ef'8 ]
            e'8 [ ]
            f'8
            fs'8
            g'8
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_spannertools_Beam__fracture_09():
    r'''Fracture container spanner to the right of index 1.
    '''

    staff = Staff(
        r'''
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
        {
            af'8
            a'8
            bf'8
            b'8
        }
        '''
        )

    beam = Beam()
    attach(beam, staff[:])
    original, left, right = beam._fracture(1, direction=Right)

    assert len(original) == 3
    assert original.components[0] is staff[0]
    assert original.components[1] is staff[1]
    assert original.components[2] is staff[2]

    assert len(left) == 2
    assert left.components[0] is staff[0]
    assert left.components[1] is staff[1]

    assert len(right) == 1
    assert right.components[0] is staff[2]

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                cs'8
                d'8
                ef'8
            }
            {
                e'8
                f'8
                fs'8
                g'8 ]
            }
            {
                af'8 [
                a'8
                bf'8
                b'8 ]
            }
        }
        '''
        )