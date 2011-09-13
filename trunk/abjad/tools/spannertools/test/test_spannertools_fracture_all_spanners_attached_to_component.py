from abjad import *


def test_spannertools_fracture_all_spanners_attached_to_component_01():
    '''Without klass keyword.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    slur = spannertools.SlurSpanner(staff.leaves)
    trill = spannertools.TrillSpanner(staff)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8
        e'8
        f'8 ] ) \stopTrillSpan
    }
    '''

    spannertools.fracture_all_spanners_attached_to_component(staff[1], 'right')

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8 ] )
        e'8 [ (
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 [ ( \\startTrillSpan\n\td'8 ] )\n\te'8 [ (\n\tf'8 ] ) \\stopTrillSpan\n}"


def test_spannertools_fracture_all_spanners_attached_to_component_02():
    '''With klass keyword.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)
    slur = spannertools.SlurSpanner(staff.leaves)
    trill = spannertools.TrillSpanner(staff)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8
        e'8
        f'8 ] ) \stopTrillSpan
    }
    '''

    spannertools.fracture_all_spanners_attached_to_component(staff[1], 'right', spannertools.BeamSpanner)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8 ]
        e'8 [
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 [ ( \\startTrillSpan\n\td'8 ]\n\te'8 [\n\tf'8 ] ) \\stopTrillSpan\n}"
