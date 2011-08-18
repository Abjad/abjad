from abjad import *


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_01():
    '''Duration split leaf in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        \time 2/8 {
            c'8 [ (
            d'8 ]
        }
        \time 2/8
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t.leaves[0], Duration(1, 32))

    r'''
    \new Staff {
        {
            \time 2/8
            c'32 ( ) [
            c'16. (
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
    assert len(halves) == 2
    assert isinstance(halves, tuple)
    assert isinstance(halves[0], list)
    assert isinstance(halves[1], list)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'32 ( ) [\n\t\tc'16. (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_02():
    '''Duration split measure in score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(1, 32))

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 7/32
            c'16. [ (
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
    assert isinstance(halves, tuple)
    assert isinstance(halves[0], list)
    assert isinstance(halves[1], list)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_03():
    '''Duration split staff outside of score and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t, Duration(1, 32))

    "halves[0][0]"

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
    }
    '''

    assert halves[0][0].format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n}"

    "halves[1][0]"

    r'''
    \new Staff {
        {
            \time 7/32
            c'16. [ (
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert halves[1][0].format == "\\new Staff {\n\t{\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_04():
    '''Duration fracture leaf in score at nonzero index.
    Fracture spanners.
    Test comes from a bug fix.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t.leaves[1], Duration(1, 32))

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32 )
            d'16. ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 )\n\t\td'16. ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_05():
    '''Duration fracture container over leaf at nonzero index.
    Fracture spanners.
    Test results from bug fix.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(7, 32))

    r'''
    \new Staff {
        {
            \time 7/32
            c'8 [ (
            d'16. ] )
        }
        {
            \time 1/32
            d'32 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 7/32\n\t\tc'8 [ (\n\t\td'16. ] )\n\t}\n\t{\n\t\t\\time 1/32\n\t\td'32 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_06():
    '''Duration split container between leaves and fracture spanners.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    parts = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(1, 8))

    r'''
    \new Staff {
        {
            \time 1/8
            c'8 [ ] ( )
        }
        {
            \time 1/8
            d'8 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert isinstance(parts, tuple)
    assert isinstance(parts[0], list)
    assert isinstance(parts[1], list)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'8 [ ] ( )\n\t}\n\t{\n\t\t\\time 1/8\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_07():
    '''Duration split leaf outside of score and fracture spanners.
    '''

    t = Note(0, (1, 8))
    spannertools.BeamSpanner(t)

    "c'8 [ ]"

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t, Duration(1, 32))

    "c'32 [ ]"
    assert componenttools.is_well_formed_component(halves[0][0])

    "c'16. [ ]"
    assert componenttools.is_well_formed_component(halves[1][0])


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_08():
    '''Duration split leaf in score and fracture spanners.
    Tie leaves after split.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    d = Duration(1, 32)
    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t.leaves[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'32 ( ) [ ~
            c'16. (
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
    assert len(halves) == 2
    assert isinstance(halves, tuple)
    assert isinstance(halves[0], list)
    assert isinstance(halves[1], list)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'32 ( ) [ ~\n\t\tc'16. (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_09():
    '''Duration split measure in score and fracture spanners.
    Tie leaves after split.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    d = Duration(1, 32)
    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( ) ~
        }
        {
            \time 7/32
            c'16. [ (
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
    assert isinstance(halves, tuple)
    assert isinstance(halves[0], list)
    assert isinstance(halves[1], list)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 7/32\n\t\tc'16. [ (\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_10():
    '''Duration split binary measure in score at nonbinary split point.
    Do fracture spanners but do not tie leaves after split.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    d = Duration(1, 5)
    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], d)

    r'''
    \new Staff {
        {
            \time 4/20
            \scaleDurations #'(4 . 5) {
                c'8 [ ( ~
                c'32
                d'16. ] ) ~
            }
        }
        {
            \time 1/20
            \scaleDurations #'(4 . 5) {
                d'16 [ ] (
            }
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ] )\n\t\t}\n\t}\n\t{\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_11():
    '''Duration split binary measure in score at nonbinary split point.
    Do fracture spanners and do tie leaves after split.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

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

    d = Duration(1, 5)
    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 4/20
            \scaleDurations #'(4 . 5) {
                c'8 [ ( ~
                c'32
                d'16. ] ) ~
            }
        }
        {
            \time 1/20
            \scaleDurations #'(4 . 5) {
                d'16 [ ] (
            }
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ] ) ~\n\t\t}\n\t}\n\t{\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_12():
    '''Split binary measure at nonbinary split point.
    Do fracture spanners but do not tie across split locus.
    This test results from a fix.
    What's being tested here is contents rederivation.
    '''

    t = Staff(Measure((3, 8), "c'8 d'8 e'8") * 2)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            \time 3/8
            c'8 [ (
            d'8
            e'8 ]
        }
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ] )
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(7, 20))

    r'''
    \new Staff {
        {
            \time 14/40
            \scaleDurations #'(4 . 5) {
                c'8 [ ( ~
                c'32
                d'8 ~
                d'32
                e'8 ] )
            }
        }
        {
            \time 1/40
            \scaleDurations #'(4 . 5) {
                e'32 [ ] (
            }
        }
        {
            \time 3/8
            c'8 [
            d'8
            e'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 14/40\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'8 ~\n\t\t\td'32\n\t\t\te'8 ] )\n\t\t}\n\t}\n\t{\n\t\t\\time 1/40\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\te'32 [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_13():
    '''Duration split leaf with LilyPond multiplier.
    Split at binary split point.
    Halves carry original written duration.
    Halves carry adjusted LilyPond multipliers.
    '''

    t = Note(0, (1, 8))
    t.duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t, Duration(1, 32))

    assert len(halves) == 2
    assert componenttools.is_well_formed_component(halves[0][0])
    assert componenttools.is_well_formed_component(halves[1][0])

    assert halves[0][0].format == "c'8 * 1/4"
    assert halves[1][0].format == "c'8 * 1/4"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_14():
    '''Duration split leaf with LilyPond multiplier.
    Split at nonbinary split point.
    Halves carry original written duration.
    Halves carry adjusted LilyPond multipliers.
    '''

    t = Note(0, (1, 8))
    t.duration_multiplier = Duration(1, 2)

    "c'8 * 1/2"

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t, Duration(1, 48))

    assert len(halves) == 2
    assert componenttools.is_well_formed_component(halves[0][0])
    assert componenttools.is_well_formed_component(halves[1][0])

    assert halves[0][0].format == "c'8 * 1/6"
    assert halves[1][0].format == "c'8 * 1/3"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_15():
    '''Duration split binary measure with multiplied leaves.
    Split at binary split point between leaves.
    Leaves remain unaltered.'''

    t = Staff(Measure((2, 16), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    for leaf in t.leaves:
        leaf.duration_multiplier = Duration(1, 2)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            \time 2/16
            c'8 * 1/2 [ (
            d'8 * 1/2 ]
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(1, 16))

    r'''
    \new Staff {
        {
            \time 1/16
            c'8 * 1/2 [ ] ( )
        }
        {
            \time 1/16
            d'8 * 1/2 [ ] (
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'8 * 1/2 [ ] ( )\n\t}\n\t{\n\t\t\\time 1/16\n\t\td'8 * 1/2 [ ] (\n\t}\n\t{\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_16():
    '''Duration split binary measure with multiplied leaves.
    Split at binary split point through leaves.
    Leaf written durations stay the same but multipliers change.
    '''

    t = Staff(Measure((2, 16), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    for leaf in t.leaves:
        leaf.duration_multiplier = Duration(1, 2)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            \time 2/16
            c'8 * 1/2 [ (
            d'8 * 1/2 ]
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(3, 32))

    r'''
    \new Staff {
        {
            \time 3/32
            c'8 * 1/2 [ (
            d'8 * 1/4 ] )
        }
        {
            \time 1/32
            d'8 * 1/4 [ ] (
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'8 * 1/2 [ (\n\t\td'8 * 1/4 ] )\n\t}\n\t{\n\t\t\\time 1/32\n\t\td'8 * 1/4 [ ] (\n\t}\n\t{\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_17():
    '''Duration split binary measure with multiplied leaves.
    Split at nonbinary split point through leaves.
    Leaf written durations adjust for binary-to-nonbinary change.
    Leaf multipliers also change.
    '''

    t = Staff(Measure((2, 16), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    for leaf in t.leaves:
        leaf.duration_multiplier = Duration(1, 2)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            \time 2/16
            c'8 * 1/2 [ (
            d'8 * 1/2 ]
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(2, 24))

    r'''
    \new Staff {
        {
            \time 2/24
            \scaleDurations #'(2 . 3) {
                c'8. * 1/2 [ (
                d'8. * 1/6 ] )
            }
        }
        {
            \time 1/24
            \scaleDurations #'(2 . 3) {
                d'8. * 1/3 [ ] (
            }
        }
        {
            \time 2/16
            e'8 * 1/2 [
            f'8 * 1/2 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8. * 1/2 [ (\n\t\t\td'8. * 1/6 ] )\n\t\t}\n\t}\n\t{\n\t\t\\time 1/24\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8. * 1/3 [ ] (\n\t\t}\n\t}\n\t{\n\t\t\\time 2/16\n\t\te'8 * 1/2 [\n\t\tf'8 * 1/2 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_18():
    '''Duration split binary measure with multiplied leaves.
    Time signature carries numerator that necessitates ties.
    Split at nonbinary split point through leaves.
    '''

    t = Staff([Measure((5, 16), [skiptools.Skip((1, 1))])])
    t.leaves[0].duration_multiplier = Duration(5, 16)

    r'''
    \new Staff {
        {
            \time 5/16
            s1 * 5/16
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(16, 80))

    r'''
    \new Staff {
        {
            \time 16/80
            \scaleDurations #'(4 . 5) {
                s1 * 1/4
            }
        }
        {
            \time 9/80
            \scaleDurations #'(4 . 5) {
                s1 * 9/64
            }
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 16/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\ts1 * 1/4\n\t\t}\n\t}\n\t{\n\t\t\\time 9/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\ts1 * 9/64\n\t\t}\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_fracture_crossing_spanners_19():
    '''Duration split nonbinary measure at nonbinary split point.
    Measure multiplier and split point multiplier match.
    Split between leaves but do fracture spanners.
    '''

    t = Staff([Measure((15, 80), notetools.make_notes(
        0, [Duration(1, 32)] * 7 + [Duration(1, 64)]))])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            \time 15/80
            \scaleDurations #'(4 . 5) {
                c'32 [ (
                d'32
                e'32
                f'32
                g'32
                a'32
                b'32
                c''64 ] )
            }
        }
    }
    '''

    halves = componenttools.split_component_at_prolated_duration_and_fracture_crossing_spanners(t[0], Duration(14, 80))

    r'''
    \new Staff {
        {
            \time 14/80
            \scaleDurations #'(4 . 5) {
                c'32 [ (
                d'32
                e'32
                f'32
                g'32
                a'32
                b'32 ] )
            }
        }
        {
            \time 1/80
            \scaleDurations #'(4 . 5) {
                c''64 [ ] ( )
            }
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(halves) == 2
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 14/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'32 [ (\n\t\t\td'32\n\t\t\te'32\n\t\t\tf'32\n\t\t\tg'32\n\t\t\ta'32\n\t\t\tb'32 ] )\n\t\t}\n\t}\n\t{\n\t\t\\time 1/80\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc''64 [ ] ( )\n\t\t}\n\t}\n}"
