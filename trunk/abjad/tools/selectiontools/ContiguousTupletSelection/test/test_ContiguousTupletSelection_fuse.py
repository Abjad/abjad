# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_ContiguousTupletSelection_fuse_01():
    r'''Fuse two unincorporated fixed-duration tuplets with same multiplier.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(t2[:])

    r'''
    \times 2/3 {
        c'8 [
        d'8
        e'8 ]
    }
    '''

    r'''
    \times 2/3 {
        c'16 (
        d'16
        e'16 )
    }
    '''

    tuplets = selectiontools.select_tuplets([t1, t2], recurse=False)
    new = tuplets.fuse()

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

    assert select(new).is_well_formed()
    assert len(t1) == 0
    assert len(t2) == 0
    assert new is not t1 and new is not t2

    assert testtools.compare(
        new.lilypond_format,
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



def test_ContiguousTupletSelection_fuse_02():
    r'''Fuse fixed-duration tuplets with same multiplier in score.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(t2[:])
    voice = Voice([t1, t2])

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

    tuplets = selectiontools.select_tuplets(voice, recurse=False)
    tuplets.fuse()

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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
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


def test_ContiguousTupletSelection_fuse_03():
    r'''Fuse fixed-multiplier tuplets with same multiplier in score.
    '''

    t1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8 g'8")
    spannertools.SlurSpanner(t2[:])
    voice = Voice([t1, t2])

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

    tuplets = selectiontools.select_tuplets(voice, recurse=False)
    tuplets.fuse()

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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
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


def test_ContiguousTupletSelection_fuse_04():
    r'''Tuplets must carry same multiplier.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8 f'8 g'8")
    tuplets = selectiontools.select_tuplets([t1, t2], recurse=False)

    assert py.test.raises(Exception, 'tuplets.fuse()')


def test_ContiguousTupletSelection_fuse_05():
    r'''Tuplets must be same type.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    tuplets = selectiontools.select_tuplets([t1, t2], recurse=False)

    assert py.test.raises(Exception, 'tuplets.fuse()')


def test_ContiguousTupletSelection_fuse_06():
    r'''Dominant spanners on contents are preserved.
    '''

    voice = Voice([
        tuplettools.FixedDurationTuplet(Duration(1, 12), [Note(0, (1, 8))]),
        tuplettools.FixedDurationTuplet(Duration(1, 6), [Note("c'4")]),
        Note("c'4")])
    spannertools.SlurSpanner(voice.select_leaves())

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

    tuplets = selectiontools.select_tuplets(voice[:2], recurse=False)
    tuplets.fuse()

    r'''
    \new Voice {
        \times 2/3 {
            c'8 (
            c'4
        }
        c'4 )
    }
    '''

    assert select(voice).is_well_formed()
    assert testtools.compare(
        voice.lilypond_format,
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
