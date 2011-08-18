from abjad import *
import py.test


def test_FixedDurationTuplet___add___01():
    '''Add two fixed-duration tuplets with same multiplier outside of score.'''

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

    new = t1 + t2

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


def test_FixedDurationTuplet___add___02():
    '''Add fixed-duration tuplets with same multiplier in score.'''

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

    t[0] + t[1]

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


def test_FixedDurationTuplet___add___03():
    '''Tuplets must carry same multiplier.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(4, 16), "c'8 d'8 e'8 f'8 g'8")
    t2 = tuplettools.FixedDurationTuplet(Duration(4, 16), "c'8 d'8 e'8 f'8 g'8 a'8")

    assert py.test.raises(TupletFuseError, 't1 + t2')
