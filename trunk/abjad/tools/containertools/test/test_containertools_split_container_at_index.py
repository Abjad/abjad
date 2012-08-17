from abjad import *
import py


def test_containertools_split_container_at_index_01():
    '''Index split tuplet in score and do not fracture spanners.'''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = beamtools.BeamSpanner(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8\n\t}\n\t\\times 2/3 {\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_02():
    '''Index split binary measure in score and do not fracture spanners.'''

    t = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = beamtools.BeamSpanner(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"



def test_containertools_split_container_at_index_03():
    '''Index split nonbinary measure in score and do not frature spanners.'''

    t = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    p = beamtools.BeamSpanner(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"
    #assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 3/9\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 1/9\n\t\t\tf'8\n\t\t}\n\t}\n\t{\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\t\\time 2/9\n\t\t\tg'8\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"


def test_containertools_split_container_at_index_04():
    '''A single container can be index split in two by the middle;
        no parent.'''

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

    assert componenttools.is_well_formed_component(t1)
    assert componenttools.is_well_formed_component(t2)
    assert t1.lilypond_format == "\\new Voice {\n\tc'8\n\td'8\n}"
    assert t2.lilypond_format == "\\new Voice {\n\te'8\n\tf'8\n}"


def test_containertools_split_container_at_index_05():
    '''A single container 'split' at index 0 gives
        an empty lefthand part and a complete righthand part.
        Original container empties contents.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    beamtools.BeamSpanner(v)
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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == '\\new Voice {\n}'
    assert right.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_06():
    '''Split container at index greater than len(container).
        Lefthand part instantiates with all contents.
        Righthand part instantiates empty.
        Original container empties contents.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    left, right = containertools.split_container_at_index(v, 10, fracture_spanners=False)

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "\\new Voice {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
    assert right.lilypond_format == '\\new Voice {\n}'
    assert v.lilypond_format == '\\new Voice {\n}'
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_containertools_split_container_at_index_07():
    '''Voice can be index split.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    #assert py.test.raises(ContiguityError, 'containertools.split_container_at_index(v, -2, fracture_spanners=False)')

    left, right = containertools.split_container_at_index(v, -2, fracture_spanners=False)
    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "\\new Voice {\n\tc'8\n\td'8\n}"
    assert right.lilypond_format == "\\new Voice {\n\te'8\n\tf'8\n}"
    assert v.lilypond_format == '\\new Voice {\n}'
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8\n\t\td'8\n\t}\n\t\\new Voice {\n\t\te'8\n\t\tf'8\n\t}\n}"


def test_containertools_split_container_at_index_08():
    '''Index split container in score and do not fracture spanners.'''

    t = Staff([Container("c'8 d'8 e'8 f'8")])
    v = t[0]
    beamtools.BeamSpanner(v)
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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "{\n\tc'8 [\n\td'8\n}"
    assert right.lilypond_format == "{\n\te'8\n\tf'8 ]\n}"
    assert v.lilypond_format == '{\n}'
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_09():
    '''Index split tuplet in score and do not fracture spanners.'''

    t = Staff([Voice([Tuplet(Fraction(4, 5), notetools.make_repeated_notes(5))])])
    v = t[0]
    tuplet = v[0]
    beamtools.BeamSpanner(tuplet)
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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "\\times 4/5 {\n\tc'8 [\n\tc'8\n}"
    assert right.lilypond_format == "\\times 4/5 {\n\tc'8\n\tc'8\n\tc'8 ]\n}"
    assert tuplet.lilypond_format == '\\times 4/5 {\n}'
    assert v.lilypond_format == "\\new Voice {\n\t\\times 4/5 {\n\t\tc'8 [\n\t\tc'8\n\t}\n\t\\times 4/5 {\n\t\tc'8\n\t\tc'8\n\t\tc'8 ]\n\t}\n}"
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\t\\times 4/5 {\n\t\t\tc'8 [\n\t\t\tc'8\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8 ]\n\t\t}\n\t}\n}"


def test_containertools_split_container_at_index_10():
    '''Index split left of leaf in score and do not fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[0])
    beamtools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.leaves)
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

    leaf = t.leaves[1]
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

    assert componenttools.is_well_formed_component(t)
    assert left is None
    assert right is leaf
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_at_index_11():
    '''Index split right of leaf in score and do not fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[0])
    beamtools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.leaves)
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

    leaf = t.leaves[1]
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

    assert componenttools.is_well_formed_component(t)
    assert left is leaf
    assert right is None
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_at_index_12():
    '''Index split triplet, and fracture spanners.'''

    t = Voice(tuplettools.FixedDurationTuplet(Duration(2, 8), notetools.make_repeated_notes(3)) * 2)
    tuplet = t[1]
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[:])

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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "\\times 2/3 {\n\tf'8 ]\n}"
    assert right.lilypond_format == "\\times 2/3 {\n\tg'8 [\n\ta'8 ]\n}"
    assert tuplet.lilypond_format == ''
    assert t.lilypond_format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8 ]\n\t}\n\t\\times 2/3 {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_13():
    '''Index split binary measure, and fracture spanners.'''

    t = Voice(Measure((3, 8), notetools.make_repeated_notes(3)) * 2)
    m = t[1]
    beamtools.BeamSpanner(t[:])
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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "{\n\t\\time 1/8\n\tf'8 ]\n}"
    assert right.lilypond_format == "{\n\t\\time 2/8\n\tg'8 [\n\ta'8 ]\n}"
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\t\\time 1/8\n\t\tf'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_14():
    '''Index split nonbinary measure, and fracture spanners.'''

    t = Voice(Measure((3, 9), notetools.make_repeated_notes(3)) * 2)
    m = t[1]
    beamtools.BeamSpanner(t[:])
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

    assert componenttools.is_well_formed_component(t)
    assert left.lilypond_format == "{\n\t\\time 1/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tf'8 ]\n\t}\n}"
    assert right.lilypond_format == "{\n\t\\time 2/9\n\t\\scaleDurations #'(8 . 9) {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
    assert py.test.raises(UnderfullContainerError, 'm.lilypond_format')
    assert t.lilypond_format == "\\new Voice {\n\t{\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t}\n\t{\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8 ]\n\t\t}\n\t}\n\t{\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8 [\n\t\t\ta'8 ]\n\t\t}\n\t}\n}"


def test_containertools_split_container_at_index_15():
    '''Index split voice outside of score.
        Fracture spanners.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(t[:])

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

    assert left.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n}"
    assert right.lilypond_format == "\\new Voice {\n\te'8\n\tf'8 ]\n}"
    assert t.lilypond_format == '\\new Voice {\n}'


def test_containertools_split_container_at_index_16():
    '''A single container 'split' at index 0 gives
        an empty lefthand part and a complete righthand part.
        Original container empties contents.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    beamtools.BeamSpanner(v)

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

    assert left.lilypond_format == '\\new Voice {\n}'
    assert right.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
    assert v.lilypond_format == '\\new Voice {\n}'
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_17():
    '''Split container at index greater than len(container).
        Lefthand part instantiates with all contents.
        Righthand part instantiates empty.
        Original container empties contents.'''

    t = Staff([Voice("c'8 d'8 e'8 f'8")])
    v = t[0]
    beamtools.BeamSpanner(v)

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

    assert left.lilypond_format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"
    assert right.lilypond_format == '\\new Voice {\n}'
    assert v.lilypond_format == '\\new Voice {\n}'
    assert t.lilypond_format == "\\new Staff {\n\t\\new Voice {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_containertools_split_container_at_index_18():
    '''Index split measure in score and fracture spanners.'''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[0])
    beamtools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.leaves)
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

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/8\n\t\td'8 [ ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_at_index_19():
    '''Index split left of leaf in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[0])
    beamtools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.leaves)
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

    leaf = t.leaves[1]
    left, right = containertools.split_container_at_index(leaf, -100, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 ( ) [
            d'8 ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert left is None
    assert right is leaf
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 ( ) [\n\t\td'8 ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_at_index_20():
    '''Index split right of leaf in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(t)
    beamtools.BeamSpanner(t[0])
    beamtools.BeamSpanner(t[1])
    slur = spannertools.SlurSpanner(t.leaves)
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

    leaf = t.leaves[1]
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

    assert componenttools.is_well_formed_component(t)
    assert left is leaf
    assert right is None
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'8 ] )\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [ (\n\t\tf'8 ] )\n\t}\n}"


def test_containertools_split_container_at_index_21():
    '''Index split nonbinary measure in score.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    t = Staff([Measure((3, 12), "c'8. d'8.")])
    beamtools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t.leaves)
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

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 3/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8. [ ] )\n\t\t}\n\t}\n}"



def test_containertools_split_container_at_index_22():
    '''Index split binary measure in score.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''

    t = Staff([Measure((3, 8), "c'8. d'8.")])
    beamtools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t.leaves)
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

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/16\n\t\tc'8. [ ] (\n\t}\n\t{\n\t\t\\time 3/16\n\t\td'8. [ ] )\n\t}\n}"
