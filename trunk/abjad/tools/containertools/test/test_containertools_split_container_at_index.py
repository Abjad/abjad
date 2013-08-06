# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_containertools_split_container_at_index_01():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8
        }
    }
    '''

    containertools.split_container_at_index(t[1], 1, fracture_spanners=False)

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            f'8
        }
        \times 2/3 {
            g'8
            a'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t}\n\t\\times 2/3 {\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_02():
    r'''Split in-score measure with power-of-two denominator and do not fracture spanners.
    '''

    t = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        {
            \time 3/8
            c'8 [
            d'8
            e'8
        }
        {
            \time 3/8
            f'8
            g'8
            a'8 ]
        }
    }
    '''

    containertools.split_container_at_index(t[1], 1, fracture_spanners=False)

    r'''
    \new Voice {
        {
            \time 3/8
            c'8 [
            d'8
            e'8
        }
        {
            \time 1/8
            f'8
        }
        {
            \time 2/8
            g'8
            a'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"
        )



def test_containertools_split_container_at_index_03():
    r'''Split in-score measure without power-of-two denominator and do not frature spanners.
    '''

    t = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                c'8 [
                d'8
                e'8
            }
        }
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                f'8
                g'8
                a'8 ]
            }
        }
    }
    '''

    containertools.split_container_at_index(t[1], 1, fracture_spanners=False)

    r'''
    \new Voice {
        {
            \time 3/9
            \scaleDurations #'(8 . 9) {
                c'8 [
                d'8
                e'8
            }
        }
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8
            }
        }
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8
                a'8 ]
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"
        )
    #assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 3/9\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 1/9\n\t\t\tf'8\n\t\t}\n\t}\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 2/9\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"


def test_containertools_split_container_at_index_04():
    r'''A single container can be index split in two by the middle; no parent.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    t1, t2 = containertools.split_container_at_index(t, 2, fracture_spanners=False)

    r'''
    \new Voice {
        c'8
        d'8
    }
    \new Voice {
        e'8
        f'8
    }
    '''

    assert select(t1).is_well_formed()
    assert select(t2).is_well_formed()
    assert testtools.compare(
        t1.lilypond_format,
        "\\new Voice {\n\tc'8\n\td'8\n}"
        )
    assert testtools.compare(
        t2.lilypond_format,
        "\\new Voice {\n\te'8\n\tf'8\n}"
        )


def test_containertools_split_container_at_index_05():
    r'''A single container 'split' at index 0 gives
    an empty lefthand part and a complete righthand part.
    Original container empties contents.
    '''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    spannertools.BeamSpanner(v)
    left, right = containertools.split_container_at_index(v, 0, fracture_spanners=False)

    r'''
    \new Staff {
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_06():
    r'''Split container at index greater than len(container).
    Lefthand part instantiates with all contents.
    Righthand part instantiates empty.
    Original container empties contents.
    '''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    left, right = containertools.split_container_at_index(v, 10, fracture_spanners=False)

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        v.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"
        )


def test_containertools_split_container_at_index_07():
    r'''Voice can be index split.
    '''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    #assert py.test.raises(ContiguityError, 'containertools.split_container_at_index(v, -2, fracture_spanners=False)')

    left, right = containertools.split_container_at_index(v, -2, fracture_spanners=False)
    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "\\new Voice {\n\tc'8\n\td'8\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\new Voice {\n\te'8\n\tf'8\n}"
        )
    assert testtools.compare(
        v.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Voice {\n\t\te'8\n\t\tf'8\n\t}\n}"
        )


def test_containertools_split_container_at_index_08():
    r'''Slit container in score and do not fracture spanners.
    '''

    t = Staff([Container("c'8 d'8 e'8 f'8")])
    v = t[0]
    spannertools.BeamSpanner(v)
    left, right = containertools.split_container_at_index(v, 2, fracture_spanners=False)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "{\n\tc'8 [\n\td'8\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "{\n\te'8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        v.lilypond_format,
        '{\n}'
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_09():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    t = Staff([Voice([Tuplet(Fraction(4, 5), notetools.make_repeated_notes(5))])])
    v = t[0]
    tuplet = v[0]
    spannertools.BeamSpanner(tuplet)
    left, right = containertools.split_container_at_index(tuplet, 2, fracture_spanners=False)

    r'''
    \new Staff {
        \new Voice {
            \times 4/5 {
                c'8 [
                c'8
            }
            \times 4/5 {
                c'8
                c'8
                c'8 ]
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "\\times 4/5 {\n\tc'8 [\n\tc'8\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\times 4/5 {\n\tc'8\n\tc'8\n\tc'8 ]\n}"
        )
    assert testtools.compare(
        tuplet.lilypond_format,
        '\\times 4/5 {\n}'
        )
    assert testtools.compare(
        v.lilypond_format,
        "\\new Voice {\n\t\\times 4/5 {\n\t\tc'8 [\n\t\tc'8\n\t}\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"
        )


def test_containertools_split_container_at_index_10():
    r'''Split left of leaf in score and do not fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    leaf = t.select_leaves()[1]
    left, right = containertools.split_container_at_index(leaf, -100, fracture_spanners=False)

    "Score is unchanged."

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert left is None
    assert right is leaf
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
        )


def test_containertools_split_container_at_index_11():
    r'''Split right of leaf in score and do not fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    leaf = t.select_leaves()[1]
    left, right = containertools.split_container_at_index(leaf, 100, fracture_spanners=False)

    "Score is unchanged."

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert left is leaf
    assert right is None
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
        )


def test_containertools_split_container_at_index_12():
    r'''Split triplet, and fracture spanners.
    '''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    tuplet = t[1]
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            f'8
            g'8
            a'8 ]
        }
    }
    '''

    left, right = containertools.split_container_at_index(tuplet, 1, fracture_spanners=True)

    r'''
    \new Voice {
        \times 2/3 {
            c'8 [
            d'8
            e'8
        }
        \times 2/3 {
            f'8 ]
        }
        \times 2/3 {
            g'8 [
            a'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "\\times 2/3 {\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\times 2/3 {\n\tg'8 [\n\ta'8 ]\n}"
        )
    assert tuplet.lilypond_format == ''
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8 ]\n\t}\n\t\\times 2/3 {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_13():
    r'''Split measure with power-of-two time signature denominator.
    Fracture spanners.
    '''

    t = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    m = t[1]
    spannertools.BeamSpanner(t[:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        {
            \time 3/8
            c'8 [
            d'8
            e'8
        }
        {
            \time 3/8
            f'8
            g'8
            a'8 ]
        }
    }
    '''

    left, right = containertools.split_container_at_index(m, 1, fracture_spanners=True)

    r'''
    \new Voice {
        {
            \time 3/8
            c'8 [
            d'8
            e'8
        }
        {
            \time 1/8
            f'8 ]
        }
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "{\n\t\\time 1/8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "{\n\t\\time 2/8\n\tg'8 [\n\ta'8 ]\n}"
        )
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_14():
    r'''Split measure without power-of-two time signature denominator.
    Fracture spanners.
    '''

    t = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    m = t[1]
    spannertools.BeamSpanner(t[:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)

    r'''
    \new Voice {
        {
            \time 3/9
            \scaleDurations '(8 . 9) {
                c'8 [
                d'8
                e'8
            }
        }
        {
            \time 3/9
            \scaleDurations '(8 . 9) {
                f'8
                g'8
                a'8 ]
            }
        }
    }
    '''

    left, right = containertools.split_container_at_index(m, 1, fracture_spanners=True)

    r'''
    \new Voice {
        {
            \time 3/9
            \scaleDurations '(8 . 9) {
                c'8 [
                d'8
                e'8
            }
        }
        {
            \time 1/9
            \scaleDurations '(8 . 9) {
                f'8 ]
            }
        }
        {
            \time 2/9
            \scaleDurations '(8 . 9) {
                g'8 [
                a'8 ]
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        left.lilypond_format,
        "{\n\t\\time 1/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tf'8 ]\n\t}\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "{\n\t\\time 2/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
        )
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert testtools.compare(
        t.lilypond_format,
        "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8 ]\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8 [\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"
        )


def test_containertools_split_container_at_index_15():
    r'''Split voice outside of score.
    Fracture spanners.
    '''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    left, right = containertools.split_container_at_index(t, 2, fracture_spanners=True)

    r'''
    \new Voice {
        c'8 [
        d'8
    }
    '''

    r'''
    \new Voice {
        e'8
        f'8 ]
    }
    '''

    assert testtools.compare(
        left.lilypond_format,
        "\\new Voice {\n\tc'8 [\n\td'8\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\new Voice {\n\te'8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        t.lilypond_format,
        '\\new Voice {\n}'
        )


def test_containertools_split_container_at_index_16():
    r'''A single container 'split' at index 0 gives
    an empty lefthand part and a complete righthand part.
    Original container empties contents.
    '''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    spannertools.BeamSpanner(v)

    r'''
    \new Staff {
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    left, right = containertools.split_container_at_index(v, 0, fracture_spanners=True)

    r'''
    \new Staff {
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    assert testtools.compare(
        left.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        right.lilypond_format,
        "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        v.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_17():
    r'''Split container at index greater than len(container).
    Lefthand part instantiates with all contents.
    Righthand part instantiates empty.
    Original container empties contents.
    '''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    spannertools.BeamSpanner(v)

    left, right = containertools.split_container_at_index(v, 10, fracture_spanners=True)

    r'''
    \new Staff {
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    assert testtools.compare(
        left.lilypond_format,
        "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
        )
    assert testtools.compare(
        right.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        v.lilypond_format,
        '\\new Voice {\n}'
        )
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
        )


def test_containertools_split_container_at_index_18():
    r'''Split measure in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    left, right = containertools.split_container_at_index(t[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 1/8
            c'8 [ ] (
        }
        {
            \time 1/8
            d'8 [ ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/8\n\t\td'8 [ ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
        )


def test_containertools_split_container_at_index_19():
    r'''Split left of leaf in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)


    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    leaf = t.select_leaves()[1]
    left, right = containertools.split_container_at_index(leaf, -100, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ ( )
            d'8 ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert left is None
    assert right is leaf
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ ( )\n\t\td'8 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
        )


def test_containertools_split_container_at_index_20():
    r'''Split right of leaf in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    leaf = t.select_leaves()[1]
    left, right = containertools.split_container_at_index(leaf, 100, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ] )
        }
        {
            \time 2/8
            e'8 [ (
            f'8 ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert left is leaf
    assert right is None
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ] )\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [ (\n\t\tf'8 ] )\n\t}\n}"
        )


def test_containertools_split_container_at_index_21():
    r'''Split in-score measure without power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    t = Staff([Measure((3, 12), "c'8. d'8.")])
    spannertools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/12
            \scaleDurations '(2 . 3) {
                c'8. [ (
                d'8. ] )
            }
        }
    }
    '''

    halves = containertools.split_container_at_index(t[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/24
            \scaleDurations '(2 . 3) {
                c'8. [ ] (
            }
        }
        {
            \time 3/24
            \scaleDurations '(2 . 3) {
                d'8. [ ] )
            }
        }
    }
    '''

    assert select(t).is_well_formed()
    assert len(halves) == 2
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8. [ ] )\n\t\t}\n\t}\n}"
        )



def test_containertools_split_container_at_index_22():
    r'''Split in-score measure with power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    t = Staff([Measure((3, 8), "c'8. d'8.")])
    spannertools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8. [ (
            d'8. ] )
        }
    }
    '''

    halves = containertools.split_container_at_index(t[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(t)

    r'''
    \new Staff {
        {
            \time 3/16
            c'8. [ ] (
        }
        {
            \time 3/16
            d'8. [ ] )
        }
    }
    '''

    assert select(t).is_well_formed()
    assert len(halves) == 2
    assert testtools.compare(
        t.lilypond_format,
        "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8. [ ] (\n\t}\n\t{\n\t\t\\time 3/16\n\t\td'8. [ ] )\n\t}\n}"
        )
