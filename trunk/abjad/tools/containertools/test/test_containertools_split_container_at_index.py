# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_containertools_split_container_at_index_01():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    p = spannertools.BeamSpanner(voice[:])

    containertools.split_container_at_index(
        voice[1], 1, fracture_spanners=False)

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_containertools_split_container_at_index_02():
    r'''Split in-score measure with power-of-two denominator and 
    do not fracture spanners.
    '''

    voice = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    p = spannertools.BeamSpanner(voice[:])

    containertools.split_container_at_index(
        voice[1], 1, fracture_spanners=False)

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_containertools_split_container_at_index_03():
    r'''Split in-score measure without power-of-two denominator 
    and do not frature spanners.
    '''

    voice = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    p = spannertools.BeamSpanner(voice[:])

    containertools.split_container_at_index(
        voice[1], 1, fracture_spanners=False)

    assert testtools.compare(
        voice,
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
        )

    assert select(voice).is_well_formed()


def test_containertools_split_container_at_index_04():
    r'''A single container can be index split in two by the middle; no parent.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    t1, t2 = containertools.split_container_at_index(
        voice, 2, fracture_spanners=False)

    assert select(voice).is_well_formed()

    assert testtools.compare(
        t1,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )

    assert select(t1).is_well_formed()

    assert testtools.compare(
        t2,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )

    assert select(t2).is_well_formed()


def test_containertools_split_container_at_index_05():
    r'''A single container 'split' at index 0 gives
    an empty lefthand part and a complete righthand part.
    Original container empties contents.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    container = staff[0]
    spannertools.BeamSpanner(container)
    left, right = containertools.split_container_at_index(
        container, 0, fracture_spanners=False)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert select(staff).is_well_formed()

    assert testtools.compare(
        left,
        r'''
        {
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )


def test_containertools_split_container_at_index_06():
    r'''Split container at index greater than len(container).
    Lefthand part instantiates with all contents.
    Righthand part instantiates empty.
    Original container empties contents.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    left, right = containertools.split_container_at_index(voice, 10, fracture_spanners=False)

    assert select(staff).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        \new Voice {
        }
        '''
        )
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
        }
        '''
        )


def test_containertools_split_container_at_index_07():
    r'''Voice can be index split.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    #assert py.test.raises(ContiguityError, 'containertools.split_container_at_index(voice, -2, fracture_spanners=False)')

    left, right = containertools.split_container_at_index(voice, -2, fracture_spanners=False)
    assert select(staff).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        \new Voice {
            c'8
            d'8
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8
            f'8
        }
        '''
        )
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                e'8
                f'8
            }
        }
        '''
        )


def test_containertools_split_container_at_index_08():
    r'''Slit container in score and do not fracture spanners.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    voice = staff[0]
    spannertools.BeamSpanner(voice)
    left, right = containertools.split_container_at_index(voice, 2, fracture_spanners=False)

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

    assert select(staff).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        {
            c'8 [
            d'8
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        {
            e'8
            f'8 ]
        }
        '''
        )
    assert testtools.compare(
        voice,
        r'''
        {
        }
        '''
        )
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_09():
    r'''Split tuplet in score and do not fracture spanners.
    '''

    staff = Staff([Voice([Tuplet(Fraction(4, 5), notetools.make_repeated_notes(5))])])
    voice = staff[0]
    tuplet = voice[0]
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

    assert select(staff).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        \times 4/5 {
            c'8 [
            c'8
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        \times 4/5 {
            c'8
            c'8
            c'8 ]
        }
        '''
        )
    assert testtools.compare(
        tuplet,
        r'''
        \times 4/5 {
        }
        '''
        )
    assert testtools.compare(
        voice,
        r'''
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
        '''
        )
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_10():
    r'''Split left of leaf in score and do not fracture spanners.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    leaf = staff.select_leaves()[1]
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

    assert select(staff).is_well_formed()
    assert left is None
    assert right is leaf
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_11():
    r'''Split right of leaf in score and do not fracture spanners.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    leaf = staff.select_leaves()[1]
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

    assert select(staff).is_well_formed()
    assert left is leaf
    assert right is None
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_12():
    r'''Split triplet, and fracture spanners.
    '''

    voice = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    tuplet = voice[1]
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    spannertools.BeamSpanner(voice[:])

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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        \times 2/3 {
            f'8 ]
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        \times 2/3 {
            g'8 [
            a'8 ]
        }
        '''
        )
    assert tuplet.lilypond_format == ''
    assert testtools.compare(
        voice,
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
        )


def test_containertools_split_container_at_index_13():
    r'''Split measure with power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    m = voice[1]
    spannertools.BeamSpanner(voice[:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        {
            \time 1/8
            f'8 ]
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        {
            \time 2/8
            g'8 [
            a'8 ]
        }
        '''
        )
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert testtools.compare(
        voice,
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
        )


def test_containertools_split_container_at_index_14():
    r'''Split measure without power-of-two time signature denominator.
    Fracture spanners.
    '''

    voice = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    m = voice[1]
    spannertools.BeamSpanner(voice[:])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)

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

    assert select(voice).is_well_formed()
    assert testtools.compare(
        left,
        r'''
        {
            \time 1/9
            \scaleDurations #'(8 . 9) {
                f'8 ]
            }
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        {
            \time 2/9
            \scaleDurations #'(8 . 9) {
                g'8 [
                a'8 ]
            }
        }
        '''
        )
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert testtools.compare(
        voice,
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
                    f'8 ]
                }
            }
            {
                \time 2/9
                \scaleDurations #'(8 . 9) {
                    g'8 [
                    a'8 ]
                }
            }
        }
        '''
        )


def test_containertools_split_container_at_index_15():
    r'''Split voice outside of score.
    Fracture spanners.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    left, right = containertools.split_container_at_index(voice, 2, fracture_spanners=True)

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
        left,
        r'''
        \new Voice {
            c'8 [
            d'8
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        \new Voice {
            e'8
            f'8 ]
        }
        '''
        )
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
        }
        '''
        )


def test_containertools_split_container_at_index_16():
    r'''A single container 'split' at index 0 gives
    an empty lefthand part and a complete righthand part.
    Original container empties contents.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    container = staff[0]
    spannertools.BeamSpanner(container)

    left, right = containertools.split_container_at_index(
        container, 0, fracture_spanners=True)

    assert testtools.compare(
        left,
        r'''
        {
        }
        '''
        )

    assert testtools.compare(
        right,
        r'''
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )

    assert testtools.compare(
        container,
        r'''
        {
        }
        '''
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )


def test_containertools_split_container_at_index_17():
    r'''Split container at index greater than len(container).
    Lefthand part instantiates with all contents.
    Righthand part instantiates empty.
    Original container empties contents.
    '''

    staff = Staff([Container("c'8 d'8 e'8 f'8")])
    container = staff[0]
    spannertools.BeamSpanner(container)

    left, right = containertools.split_container_at_index(container, 10, fracture_spanners=True)

    r'''
    \new Staff {
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
    }
    '''

    assert testtools.compare(
        left,
        r'''
        {
            c'8 [
            d'8
            e'8
            f'8 ]
        }
        '''
        )
    assert testtools.compare(
        right,
        r'''
        {
        }
        '''
        )
    assert testtools.compare(
        container,
        r'''
        {
        }
        '''
        )
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                c'8 [
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )


def test_containertools_split_container_at_index_18():
    r'''Split measure in score and fracture spanners.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    left, right = containertools.split_container_at_index(staff[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_19():
    r'''Split left of leaf in score and fracture spanners.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)


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

    leaf = staff.select_leaves()[1]
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

    assert select(staff).is_well_formed()
    assert left is None
    assert right is leaf
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_20():
    r'''Split right of leaf in score and fracture spanners.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BeamSpanner(staff[0])
    spannertools.BeamSpanner(staff[1])
    slur = spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    leaf = staff.select_leaves()[1]
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

    assert select(staff).is_well_formed()
    assert left is leaf
    assert right is None
    assert testtools.compare(
        staff,
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
        )


def test_containertools_split_container_at_index_21():
    r'''Split in-score measure without power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    staff = Staff([Measure((3, 12), "c'8. d'8.")])
    spannertools.BeamSpanner(staff[0])
    spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    halves = containertools.split_container_at_index(staff[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    assert select(staff).is_well_formed()
    assert len(halves) == 2
    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    c'8. [ ] (
                }
            }
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    d'8. [ ] )
                }
            }
        }
        '''
        )



def test_containertools_split_container_at_index_22():
    r'''Split in-score measure with power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    staff = Staff([Measure((3, 8), "c'8. d'8.")])
    spannertools.BeamSpanner(staff[0])
    spannertools.SlurSpanner(staff.select_leaves())
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8. [ (
            d'8. ] )
        }
    }
    '''

    halves = containertools.split_container_at_index(staff[0], 1, fracture_spanners=True)
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

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

    assert select(staff).is_well_formed()
    assert len(halves) == 2
    assert testtools.compare(
        staff,
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
        )
