from abjad import *


def test_spannertools_fracture_spanners_attached_to_component_01():
    '''Without klass keyword.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)
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

    spannertools.fracture_spanners_attached_to_component(staff[1], direction=Right)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8 ] )
        e'8 [ (
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ( \\startTrillSpan\n\td'8 ] )\n\te'8 [ (\n\tf'8 ] ) \\stopTrillSpan\n}"


def test_spannertools_fracture_spanners_attached_to_component_02():
    '''With klass keyword.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = beamtools.BeamSpanner(staff.leaves)
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

    spannertools.fracture_spanners_attached_to_component(staff[1], direction=Right, klass=beamtools.BeamSpanner)

    r'''
    \new Staff {
        c'8 [ ( \startTrillSpan
        d'8 ]
        e'8 [
        f'8 ] ) \stopTrillSpan
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ( \\startTrillSpan\n\td'8 ]\n\te'8 [\n\tf'8 ] ) \\stopTrillSpan\n}"
