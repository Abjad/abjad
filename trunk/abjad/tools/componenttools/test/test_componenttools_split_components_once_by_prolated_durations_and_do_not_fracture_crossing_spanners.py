from abjad import *


def test_componenttools_split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners_01():
    '''Duration partition one container in score
        Do no fracture spanners.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
    parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:1], durations)

    r'''
    \new Staff {
        {
            c'32 [ (
        }
        {
            c'16.
        }
        {
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''


    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 3
    assert t.format == "\\new Staff {\n\t{\n\t\tc'32 [ (\n\t}\n\t{\n\t\tc'16.\n\t}\n\t{\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners_02():
    '''Duration partition multiple containers in score.
        Do not fracture spanners.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t[0])
    spannertools.BeamSpanner(t[1])
    spannertools.SlurSpanner(t.leaves)

    r'''
    \new Staff {
        {
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    durations = [Duration(1, 32), Duration(3, 32), Duration(5, 32)]
    parts = componenttools.split_components_once_by_prolated_durations_and_do_not_fracture_crossing_spanners(t[:], durations)

    r'''
    \new Staff {
        {
            c'32 [ (
        }
        {
            c'16.
        }
        {
            d'8 ]
        }
        {
            e'32 [
        }
        {
            e'16.
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert len(parts) == 4
    assert t.format == "\\new Staff {\n\t{\n\t\tc'32 [ (\n\t}\n\t{\n\t\tc'16.\n\t}\n\t{\n\t\td'8 ]\n\t}\n\t{\n\t\te'32 [\n\t}\n\t{\n\t\te'16.\n\t\tf'8 ] )\n\t}\n}"
