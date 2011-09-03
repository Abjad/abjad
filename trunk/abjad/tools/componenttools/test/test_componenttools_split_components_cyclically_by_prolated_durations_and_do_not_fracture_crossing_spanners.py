from abjad import *


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_01():
    '''Cyclically duration partition one leaf in score.  Do not fracture spanners.
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

    durations = [Duration(3, 64)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[0][1:2], durations)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32.
            d'32. ~
            d'64 ~
            d'64 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 3
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32.\n\t\td'32. ~\n\t\td'64 ~\n\t\td'64 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_02():
    '''Cyclically duration partition multiple leaves in score.  Do not fracture spanners.
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

    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(t.leaves, durations)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16. [ (
            c'32
            d'16
            d'16 ]
        }
        {
            \time 2/8
            e'32 [
            e'16.
            f'16.
            f'32 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. [ (\n\t\tc'32\n\t\td'16\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'32 [\n\t\te'16.\n\t\tf'16.\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_03():
    '''Cyclically duration partition one measure in score.  Do not fracture spanners.
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

    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:1], durations)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
            \time 3/32
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 3
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_04():
    '''Cyclically duration partition multiple measures in score.  Do not fracture spanners.
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

    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:], durations)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
            \time 3/32
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 1/32
            e'32 [
        }
        {
            \time 3/32
            e'16.
        }
        {
            \time 3/32
            f'16.
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_05():
    '''Cyclically duration partition list of leaves outside of score.
    '''

    leaves = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(leaves, durations)

    assert len(parts) == 6

    t = Staff([])
    for part in parts:
        t.extend(part)

    r'''
    \new Staff {
        c'16.
        c'32
        d'16
        d'16
        e'32
        e'16.
        f'16.
        f'32
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'16.\n\tc'32\n\td'16\n\td'16\n\te'32\n\te'16.\n\tf'16.\n\tf'32\n}"


# TODO: Fix cyclic duration partition bug with spanners on outside-of-score measures #

def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_06():
    '''Cyclically duration partition list of measures outside of score.  Do not fracture spanners.
    '''

    measures = Measure((2, 8), notetools.make_repeated_notes(2)) * 2
    spannertools.BeamSpanner(measures[0])
    spannertools.BeamSpanner(measures[1])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(measures)

    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(measures, durations)

    assert len(parts) == 6

    t = Staff([])
    for part in parts:
        t.extend(part)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16.
        }
        {
            \time 3/32
            c'32
            d'16
        }
        {
            \time 2/32
            d'16 [ ]
        }
        {
            \time 1/32
            e'32
        }
        {
            \time 3/32
            e'16.
        }
        {
            \time 3/32
            f'16.
        }
        {
            \time 1/32
            f'32 [ ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16.\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ]\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_07():
    '''Duration partition one leaf in score.  Read durations cyclically in list.
    Do not fracture spanners. Do add tie after each split.
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

    durations = [Duration(1, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        t[0][1:], durations, tie_after = True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32 ~
            d'32 ~
            d'32 ~
            d'32 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 4
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_08():
    '''Duration partition multiple leaves in score.
    Read durations cyclically in list.
    Do not fracture spanners. Do add tie after each leaf split.
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

    durations = [Duration(1, 16)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        t.leaves, durations, tie_after = True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16 [ ( ~
            c'16
            d'16 ~
            d'16 ]
        }
        {
            \time 2/8
            e'16 [ ~
            e'16
            f'16 ~
            f'16 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 8
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [ ( ~\n\t\tc'16\n\t\td'16 ~\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'16 [ ~\n\t\te'16\n\t\tf'16 ~\n\t\tf'16 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_09():
    '''Duration partition one measure in score.
    Read durations cyclically in list.
    Do not fracture spanners. Do add tie after each leaf split.
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

    durations = [Duration(1, 16)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        t[:1], durations, tie_after = True)

    r'''
    \new Staff {
        {
            \time 1/16
            c'16 [ ( ~
        }
        {
            \time 1/16
            c'16
        }
        {
            \time 1/16
            d'16 ~
        }
        {
            \time 1/16
            d'16 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 4
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ( ~\n\t}\n\t{\n\t\t\\time 1/16\n\t\tc'16\n\t}\n\t{\n\t\t\\time 1/16\n\t\td'16 ~\n\t}\n\t{\n\t\t\\time 1/16\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners_10():
    '''Duration partition multiple measures in score.
    Read durations cyclically in list.
    Do not fracture spanners. Do add tie after each leaf split.
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

    durations = [Duration(3, 32)]
    parts = componenttools.split_components_cyclically_by_prolated_durations_and_do_not_fracture_crossing_spanners(
        t[:], durations, tie_after = True)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ( ~
        }
        {
            \time 3/32
            c'32
            d'16 ~
        }
        {
            \time 2/32
            d'16 ]
        }
        {
            \time 1/32
            e'32 [ ~
        }
        {
            \time 3/32
            e'16.
        }
        {
            \time 3/32
            f'16. ~
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 6
    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ( ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'32\n\t\td'16 ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\t\\time 3/32\n\t\tf'16. ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"
