from abjad import *
import py.test


def test_tuplettools_fuse_tuplets_01():
    '''Fuse two unincorporated fixed-duration tuplets with same multiplier.'''

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

    new = tuplettools.fuse_tuplets([t1, t2])

    assert componenttools.is_well_formed_component(new)
    assert len(t1) == 0
    assert len(t2) == 0
    assert new is not t1 and new is not t2

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

    assert new.format == "\\times 2/3 {\n\tc'8 [\n\td'8\n\te'8 ]\n\tc'16 (\n\td'16\n\te'16 )\n}"



def test_tuplettools_fuse_tuplets_02():
    '''Fuse fixed-duration tuplets with same multiplier in score.'''

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

    tuplettools.fuse_tuplets(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t\tc'16 (\n\t\td'16\n\t\te'16 )\n\t}\n}"


def test_tuplettools_fuse_tuplets_03():
    '''Fuse fixed-multiplier tuplets with same multiplier in score.'''

    #t1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    t1 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    spannertools.BeamSpanner(t1[:])
    #t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8 f'8 g'8")
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

    tuplettools.fuse_tuplets(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8 ]\n\t\tc'8 (\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8 )\n\t}\n}"


def test_tuplettools_fuse_tuplets_04():
    '''Tuplets must carry same multiplier.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8 f'8 g'8")

    assert py.test.raises(TupletFuseError, 'tuplettools.fuse_tuplets([t1, t2])')


def test_tuplettools_fuse_tuplets_05():
    '''Tuplets must be same type.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
    #t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
    t2 = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")

    assert py.test.raises(TupletFuseError, 'tuplettools.fuse_tuplets([t1, t2])')


def test_tuplettools_fuse_tuplets_06():
    '''Dominant spanners on contents are preserved.'''

    t = Voice([
        tuplettools.FixedDurationTuplet(Duration(1, 12), [Note(0, (1, 8))]),
        tuplettools.FixedDurationTuplet(Duration(1, 6), [Note("c'4")]),
        Note("c'4")])
    spannertools.SlurSpanner(t.leaves)

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

    tuplettools.fuse_tuplets(t[:2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8 (
            c'4
        }
        c'4 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 (\n\t\tc'4\n\t}\n\tc'4 )\n}"
