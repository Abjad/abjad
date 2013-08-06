# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_FreeTupletSelection_fuse_01():
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

    tuplets = selectiontools.select_tuplets([t1, t2])
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
        "\\times 2/3 {\n\tc'8 [\n\td'8\n\te'8 ]\n\tc'16 (\n\td'16\n\te'16 )\n}"
        )



def test_FreeTupletSelection_fuse_02():
    r'''Fuse fixed-duration tuplets with same multiplier in score.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 16), "c'16 d'16 e'16")
    spannertools.SlurSpanner(t2[:])
    t = Voice([t1, t2])

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

    tuplets = selectiontools.select_tuplets(t)
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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t\tc'16 (\n\t\td'16\n\t\te'16 )\n\t}\n}"
        )


def test_FreeTupletSelection_fuse_03():
    r'''Fuse fixed-multiplier tuplets with same multiplier in score.
    '''

    t1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8 g'8")
    spannertools.SlurSpanner(t2[:])
    t = Voice([t1, t2])

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

    tuplets = selectiontools.select_tuplets(t)
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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t\tc'8 (\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8 )\n\t}\n}"
        )


def test_FreeTupletSelection_fuse_04():
    r'''Tuplets must carry same multiplier.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8 f'8 g'8")
    tuplets = selectiontools.select_tuplets([t1, t2])

    assert py.test.raises(Exception, 'tuplets.fuse()')


def test_FreeTupletSelection_fuse_05():
    r'''Tuplets must be same type.
    '''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    tuplets = selectiontools.select_tuplets([t1, t2])

    assert py.test.raises(Exception, 'tuplets.fuse()')


def test_FreeTupletSelection_fuse_06():
    r'''Dominant spanners on contents are preserved.
    '''

    t = Voice([
        tuplettools.FixedDurationTuplet(Duration(1, 12), [Note(0, (1, 8))]),
        tuplettools.FixedDurationTuplet(Duration(1, 6), [Note("c'4")]),
        Note("c'4")])
    spannertools.SlurSpanner(t.select_leaves())

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

    tuplets = selectiontools.select_tuplets(t[:2])
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

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 (\n\t\tc'4\n\t}\n\tc'4 )\n}"
        )
