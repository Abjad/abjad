from abjad import *


def test_componenttools_split_components_at_offsets_01():
    '''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[0][1:2], [(3, 64)], cyclic=True, fracture_spanners=False)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32. ~
            d'32. ~
            d'32 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32. ~\n\t\td'32. ~\n\t\td'32 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_02():
    '''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff.leaves, [(3, 32)], cyclic=True, fracture_spanners=False)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16. [ ( ~
            c'32
            d'16. ~
            d'32 ]
        }
        {
            e'16. [ ~
            e'32
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. [ ( ~\n\t\tc'32\n\t\td'16 ~\n\t\td'16 ]\n\t}\n\t{\n\t\te'32 [ ~\n\t\te'16.\n\t\tf'16. ~\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_03():
    '''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(3, 32)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
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

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_04():
    '''Cyclically split consecutive measures in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ (
        }
        {
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
            f'16.
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ (\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_05():
    '''Cyclically split orphan measures. Don't fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    beamtools.apply_beam_spanners_to_measures_in_expr(measures)

    parts = componenttools.split_components_at_offsets(measures, [(3, 32)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=False)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [
        }
        {
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
            f'16.
        }
        {
            \time 1/32
            f'32 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [\n\t}\n\t{\n\t\tc'32\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16.\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ]\n\t}\n}"


def test_componenttools_split_components_at_offsets_06():
    '''Cyclically split note in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[0][1:], [(1, 32)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

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
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ~\n\t\td'32 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_07():
    '''Cyclically split consecutive notes in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff.leaves, [(1, 16)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

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
            e'16 [ ~
            e'16
            f'16 ~
            f'16 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 8
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 [ ( ~\n\t\tc'16\n\t\td'16 ~\n\t\td'16 ]\n\t}\n\t{\n\t\te'16 [ ~\n\t\te'16\n\t\tf'16 ~\n\t\tf'16 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_08():
    '''Cyclically split measure in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(1, 16)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 1/16
            c'16 [ ( ~
        }
        {
            c'16
        }
        {
            d'16 ~
        }
        {
            d'16 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ( ~\n\t}\n\t{\n\t\tc'16\n\t}\n\t{\n\t\td'16 ~\n\t}\n\t{\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_09():
    '''Cyclically split consecutive measures in score. Don't fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)], 
        cyclic=True, fracture_spanners=False, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ( ~
        }
        {
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
            f'16. ~
        }
        {
            \time 1/32
            f'32 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ( ~\n\t}\n\t{\n\t\tc'32\n\t\td'16 ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16.\n\t}\n\t{\n\t\tf'16. ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_10():
    '''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[0][1:2], [(3, 64)], cyclic=True, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32. )
            d'32. ( )
            d'64 ( ~
            d'64 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32. ) ~\n\t\td'32. ( ) ~\n\t\td'32 ] (\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_11():
    '''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff.leaves, [(3, 32)], cyclic=True, fracture_spanners=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16. ( ) [
            c'32 (
            d'16 )
            d'16 ] (
        }
        {
            e'32 ) [
            e'16. (
            f'16. )
            f'32 ] ( )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16. ( ) [ ~\n\t\tc'32 (\n\t\td'16 ) ~\n\t\td'16 ] (\n\t}\n\t{\n\t\te'32 ) [ ~\n\t\te'16. (\n\t\tf'16. ) ~\n\t\tf'32 ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_12():
    '''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(3, 32)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            c'32 [ (
            d'16 ] )
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_13():
    '''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            c'32 [ (
            d'16 ] )
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] )
        }
        {
            \time 3/32
            e'16. [ ] ( )
        }
        {
            f'16. [ ] ( )
        }
        {
            \time 1/32
            f'32 [ ] ( )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] )\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\tf'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_14():
    '''Cyclically split orphan notes.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    parts = componenttools.split_components_at_offsets(
        notes, [(3, 32)], cyclic=True, fracture_spanners=True)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        c'16. ~
        c'32
        d'16 ~
        d'16
        e'32 ~
        e'16.
        f'16. ~
        f'32
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\tc'16. ~\n\tc'32\n\td'16 ~\n\td'16\n\te'32 ~\n\te'16.\n\tf'16. ~\n\tf'32\n}"


def test_componenttools_split_components_at_offsets_15():
    '''Cyclically split orphan measures. Fracture spanners.
    '''

    measures = [Measure((2, 8), "c'8 d'8"), Measure((2, 8), "e'8 f'8")]
    beamtools.apply_beam_spanners_to_measures_in_expr(measures)

    parts = componenttools.split_components_at_offsets(measures, [(3, 32)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=False)

    music = sequencetools.flatten_sequence(parts)
    staff = Staff(music)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ]
        }
        {
            c'32 [
            d'16 ]
        }
        {
            \time 2/32
            d'16 [ ]
        }
        {
            \time 1/32
            e'32 [ ]
        }
        {
            \time 3/32
            e'16. [ ]
        }
        {
            f'16. [ ]
        }
        {
            \time 1/32
            f'32 [ ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ]\n\t}\n\t{\n\t\tc'32 [\n\t\td'16 ]\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ]\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ]\n\t}\n\t{\n\t\tf'16. [ ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ]\n\t}\n}"


def test_componenttools_split_components_at_offsets_16():
    '''Cyclically split note in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[0][1:], [(1, 32)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'32 ) ~
            d'32 ( ) ~
            d'32 ( ) ~
            d'32 ] (
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [ (\n\t\td'32 ) ~\n\t\td'32 ( ) ~\n\t\td'32 ( ) ~\n\t\td'32 ] (\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_17():
    '''Cyclically split consecutive notes in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff.leaves, [(1, 16)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 2/8
            c'16 ( ) [ ~
            c'16 (
            d'16 ) ~
            d'16 ] (
        }
        {
            e'16 ) [ ~
            e'16 (
            f'16 ) ~
            f'16 ] ( )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 8
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'16 ( ) [ ~\n\t\tc'16 (\n\t\td'16 ) ~\n\t\td'16 ] (\n\t}\n\t{\n\t\te'16 ) [ ~\n\t\te'16 (\n\t\tf'16 ) ~\n\t\tf'16 ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_18():
    '''Cyclically split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:1], [(1, 16)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 1/16
            c'16 [ ] ( ) ~
        }
        {
            c'16 [ ] ( )
        }
        {
            d'16 [ ] ( ) ~
        }
        {
            d'16 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\tc'16 [ ] ( ) ~\n\t}\n\t{\n\t\tc'16 [ ] ( )\n\t}\n\t{\n\t\td'16 [ ] ( ) ~\n\t}\n\t{\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_19():
    '''Cyclically split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(staff[:], [(3, 32)], 
        cyclic=True, fracture_spanners=True, tie_split_notes=True)

    r'''
    \new Staff {
        {
            \time 3/32
            c'16. [ ] ( ) ~
        }
        {
            c'32 [ (
            d'16 ] ) ~
        }
        {
            \time 2/32
            d'16 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] ) ~
        }
        {
            \time 3/32
            e'16. [ ] ( )
        }
        {
            f'16. [ ] ( ) ~
        }
        {
            \time 1/32
            f'32 [ ] ( )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 6
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( ) ~\n\t}\n\t{\n\t\tc'32 [ (\n\t\td'16 ] ) ~\n\t}\n\t{\n\t\t\\time 2/32\n\t\td'16 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] ) ~\n\t}\n\t{\n\t\t\\time 3/32\n\t\te'16. [ ] ( )\n\t}\n\t{\n\t\tf'16. [ ] ( ) ~\n\t}\n\t{\n\t\t\\time 1/32\n\t\tf'32 [ ] ( )\n\t}\n}"


def test_componenttools_split_components_at_offsets_20():
    '''Force split measure in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:1], [(1, 32), (3, 32), (5, 32)], 
        cyclic=False, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
        {
            \time 3/32
            c'16.
        }
        {
            \time 4/32
            d'8 ]
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16.\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_21():
    '''Force split consecutive measures in score. Do not fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

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

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 32), (3, 32), (5, 32)], 
        cyclic=False, fracture_spanners=False, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ (
        }
        {
            \time 3/32
            c'16.
        }
        {
            \time 4/32
            d'8 ]
        }
        {
            \time 1/32
            e'32 [
        }
        {
            \time 7/32
            e'16.
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ (\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16.\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [\n\t}\n\t{\n\t\t\\time 7/32\n\t\te'16.\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_22():
    '''Force split measure in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:1], [(1, 32), (3, 32), (5, 32)], 
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            \time 4/32
            d'8 [ ] (
        }
        {
            \time 2/8
            e'8 [
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_23():
    '''Force split consecutive measures in score. Fracture spanners.
    '''

    staff = Staff(r"abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 |")
    beamtools.apply_beam_spanners_to_measures_in_expr(staff)
    spannertools.SlurSpanner(staff.leaves)

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [ (
            d'8 ]
        }
        {
            e'8 [
            f'8 ] )
        }
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 32), (3, 32), (5, 32)], 
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        {
            \time 1/32
            c'32 [ ] ( )
        }
        {
            \time 3/32
            c'16. [ ] ( )
        }
        {
            \time 4/32
            d'8 [ ] (
        }
        {
            \time 1/32
            e'32 [ ] )
        }
        {
            \time 7/32
            e'16. [ (
            f'8 ] )
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 4
    assert staff.lilypond_format == "\\new Staff {\n\t{\n\t\t\\time 1/32\n\t\tc'32 [ ] ( )\n\t}\n\t{\n\t\t\\time 3/32\n\t\tc'16. [ ] ( )\n\t}\n\t{\n\t\t\\time 4/32\n\t\td'8 [ ] (\n\t}\n\t{\n\t\t\\time 1/32\n\t\te'32 [ ] )\n\t}\n\t{\n\t\t\\time 7/32\n\t\te'16. [ (\n\t\tf'8 ] )\n\t}\n}"


def test_componenttools_split_components_at_offsets_24():
    '''Force split orphan note. Offsets sum to less than note duration.
    '''

    note = Note("c'4")

    parts = componenttools.split_components_at_offsets(
        [note], [(1, 32), (5, 32)], 
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    notes = sequencetools.flatten_sequence(parts)
    staff = Staff(notes)

    r'''
    \new Staff {
        c'32 ~
        c'8 ~
        c'32 ~
        c'16
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert len(parts) == 3
    assert staff.lilypond_format == "\\new Staff {\n\tc'32 ~\n\tc'8 ~\n\tc'32 ~\n\tc'16\n}"


def test_componenttools_split_components_at_offsets_25():
    '''Force split note in score. Fracture spanners.
    '''

    staff = Staff("c'8 [ ]")

    r'''
    \new Staff {
        c'8 [ ]
    }
    '''

    parts = componenttools.split_components_at_offsets(
        staff[:], [(1, 64), (5, 64)], 
        cyclic=False, fracture_spanners=True, tie_split_notes=False)

    r'''
    \new Staff {
        c'64 [ ]
        c'16 [ ~
        c'64 ] ~
        c'32 [ ]
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'64 [ ] ~\n\tc'16 [ ~\n\tc'64 ] ~\n\tc'32 [ ]\n}"
