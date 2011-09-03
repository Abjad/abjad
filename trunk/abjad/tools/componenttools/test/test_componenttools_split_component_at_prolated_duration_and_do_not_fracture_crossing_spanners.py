from abjad import *


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_01():

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

    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t.leaves[0], Duration(1, 32))

    r'''
    \new Staff {
        {
            \time 2/8
            c'32 [ (
            c'16.
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
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'32 [ (\n\t\tc'16.\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_02():

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

    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t[0], Duration(1, 32))

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
        {
            \time 7/32
            c'16.
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
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n\t{\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_03():

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

    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t, Duration(1, 32))

    "halves[0][0]"

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
    }
    '''

    assert halves[0][0].format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n}"

    "halves[1][0]"

    r'''
    \new Staff {
        {
            \time 7/32
            c'16.
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert halves[1][0].format == "\\new Staff {\n\t{\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_04():
    '''Duration split one leaf in score.
        Do not fracture spanners. But do tie after split.'''

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
    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t.leaves[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'32 [ ( ~
            c'16.
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
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'32 [ ( ~\n\t\tc'16.\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_05():
    '''Duration split one measure in score.
        Do not fracture spanners. But do add tie after split.'''

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
    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ( ~
        }
        {
            \time 7/32
            c'16.
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
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ( ~\n\t}\n\t{\n\t\t\\time 7/32\n\t\tc'16.\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_06():
    '''Duration split binary measure in score at nonbinary split point.
        Do not fracture spanners and do not tie leaves after split.'''

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
    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t[0], d)

    r'''
    \new Staff {
        {
            \time 4/20
            \scaleDurations #'(4 . 5) {
                c'8 [ ( ~
                c'32
                d'16. ~ # tie here is a bug
            }
        }
        {
            \time 1/20
            \scaleDurations #'(4 . 5) {
                d'16 ]
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
    # TODO: The tie at the split locus here is a (small) bug. #
    #         Eventually should fix. #


def test_componenttools_split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners_07():
    '''Duration split binary measure in score at nonbinary split point.
        Do fracture spanners and do tie leaves after split.'''

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
    halves = componenttools.split_component_at_prolated_duration_and_do_not_fracture_crossing_spanners(t[0], d, tie_after = True)

    r'''
    \new Staff {
        {
            \time 4/20
            \scaleDurations #'(4 . 5) {
                c'8 [ ( ~
                c'32
                d'16. ~
            }
        }
        {
            \time 1/20
            \scaleDurations #'(4 . 5) {
                d'16 ]
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
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 4/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\tc'8 [ ( ~\n\t\t\tc'32\n\t\t\td'16. ~\n\t\t}\n\t}\n\t{\n\t\t\\time 1/20\n\t\t\\scaleDurations #'(4 . 5) {\n\t\t\td'16 ]\n\t\t}\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"
