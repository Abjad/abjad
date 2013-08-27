# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_ContiguousSelection_fuse_tuplets_01():
    r'''Fuse two unincorporated fixed-duration tuplets with same multiplier.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(t2[:])

    assert testtools.compare(
        t1,
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    assert testtools.compare(
        t2,
        r'''
        \times 2/3 {
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    tuplets = select([t1, t2], contiguous=True)
    new = tuplets.fuse_tuplets()

    assert testtools.compare(
        new,
        r'''
        \times 2/3 {
            c'8 [
            d'8
            e'8 ]
            c'16 (
            d'16
            e'16 )
        }
        '''
        )

    assert len(t1) == 0
    assert len(t2) == 0
    assert new is not t1 and new is not t2
    assert inspect(new).is_well_formed()


def test_ContiguousSelection_fuse_tuplets_02():
    r'''Fuse fixed-duration tuplets with same multiplier in score.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(t2[:])
    voice = Voice([t1, t2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    tuplets = voice[:]
    tuplets.fuse_tuplets()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'16 (
                d'16
                e'16 )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_ContiguousSelection_fuse_tuplets_03():
    r'''Fuse fixed-multiplier tuplets with same multiplier in score.
    '''

    t1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8 g'8")
    spannertools.SlurSpanner(t2[:])
    voice = Voice([t1, t2])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
            }
            \times 2/3 {
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    tuplets = voice[:]
    tuplets.fuse_tuplets()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 [
                d'8
                e'8 ]
                c'8 (
                d'8
                e'8
                f'8
                g'8 )
            }
        }
        '''
        )

    assert inspect(voice).is_well_formed()


def test_ContiguousSelection_fuse_tuplets_04():
    r'''Tuplets must carry same multiplier.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8 f'8 g'8")
    tuplets = select([t1, t2], contiguous=True)

    assert py.test.raises(Exception, 'tuplets.fuse_tuplets()')


def test_ContiguousSelection_fuse_tuplets_05():
    r'''Tuplets must be same type.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    tuplets = select([t1, t2], contiguous=True)

    assert py.test.raises(Exception, 'tuplets.fuse_tuplets()')


def test_ContiguousSelection_fuse_tuplets_06():
    r'''Dominant spanners on contents are preserved.
    '''

    voice = Voice([
        tuplettools.FixedDurationTuplet(Duration(1, 12), [Note(0, (1, 8))]),
        tuplettools.FixedDurationTuplet(Duration(1, 6), [Note("c'4")]),
        Note("c'4")])
    spannertools.SlurSpanner(voice.select_leaves())

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 (
            }
            \times 2/3 {
                c'4
            }
            c'4 )
        }
        '''
        )

    tuplets = voice[:2]
    tuplets.fuse_tuplets()

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \times 2/3 {
                c'8 (
                c'4
            }
            c'4 )
        }
        '''
        )

    assert inspect(voice).is_well_formed()
