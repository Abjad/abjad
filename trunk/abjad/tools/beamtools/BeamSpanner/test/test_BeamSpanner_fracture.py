from abjad import *


def test_BeamSpanner_fracture_01():
    '''This test shows that fracurting beyond the *first* leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:4])
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    assert old.components == tuple(t[:4])
    old.fracture(0, direction=Left)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1


def test_BeamSpanner_fracture_02():

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:4])
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    assert old.components == tuple(t[:4])
    old.fracture(1, direction=Left)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 2


def test_BeamSpanner_fracture_03():
    '''This test shows that fracurting beyond the *last* leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:4])
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    assert old.components == tuple(t[:4])
    old.fracture(-1, direction=Right)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1


def test_BeamSpanner_fracture_04():
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:4])
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 1
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    assert old.components == tuple(t[:4])
    old.fracture(1, direction=Right)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 2


def test_BeamSpanner_fracture_05():
    '''Fracture "both" fractures around leaf.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:5])
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    old.fracture(2, direction=None)
    assert len(beamtools.get_beam_spanner_attached_to_component(t[0])) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(t[2])) == 1
    assert len(beamtools.get_beam_spanner_attached_to_component(t[3])) == 2
    assert beamtools.get_beam_spanner_attached_to_component(t[0]) != beamtools.get_beam_spanner_attached_to_component(t[2])
    assert beamtools.get_beam_spanner_attached_to_component(t[2]) != beamtools.get_beam_spanner_attached_to_component(t[3])

    componenttools.is_well_formed_component(t) # check for Beam overlaps
    assert t.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8 ]\n\td'8 [ ]\n\tef'8 [\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"

    r'''
    \new Staff {
        c'8 [
        cs'8 ]
        d'8 [ ]
        ef'8 [
        e'8 ]
        f'8
        fs'8
        g'8
    }
    '''


def test_BeamSpanner_fracture_06():
    '''Fracture "both" works of first spanned leaf.
    '''
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:5])
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    old.fracture(0, direction=None)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(t[0])) == 1
    assert len(beamtools.get_beam_spanner_attached_to_component(t[1])) == 4
    assert beamtools.get_beam_spanner_attached_to_component(t[0]) != beamtools.get_beam_spanner_attached_to_component(t[1])
    componenttools.is_well_formed_component(t) # check for Beam overlaps
    assert t.lilypond_format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8 [\n\td'8\n\tef'8\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"
    r'''
    \new Staff {
        c'8 [ ]
        cs'8 [
        d'8
        ef'8
        e'8 ]
        f'8
        fs'8
        g'8
    }
    '''


def test_BeamSpanner_fracture_07():
    '''Fracture "both" works of last spanned leaf.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:5])
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    old.fracture(4, direction=None)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(t[0])) == 4
    assert len(beamtools.get_beam_spanner_attached_to_component(t[4])) == 1
    assert beamtools.get_beam_spanner_attached_to_component(t[0]) != beamtools.get_beam_spanner_attached_to_component(t[4])
    componenttools.is_well_formed_component(t) # check for Beam overlaps
    assert t.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        e'8 [ ]
        f'8
        fs'8
        g'8
    }
    '''


def test_BeamSpanner_fracture_08():
    '''Fracture "both" works with negative indices.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(8)])
    beamtools.BeamSpanner(t[:5])
    old = list(spannertools.get_spanners_attached_to_any_improper_child_of_component(t))[0]
    old.fracture(-1, direction=None)
    assert len(spannertools.get_spanners_attached_to_any_improper_child_of_component(t)) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(t[0])) == 4
    assert len(beamtools.get_beam_spanner_attached_to_component(t[4])) == 1
    assert beamtools.get_beam_spanner_attached_to_component(t[0]) != beamtools.get_beam_spanner_attached_to_component(t[4])
    componenttools.is_well_formed_component(t) # check for Beam overlaps
    assert t.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"

    r'''
    \new Staff {
        c'8 [
        cs'8
        d'8
        ef'8 ]
        e'8 [ ]
        f'8
        fs'8
        g'8
    }
    '''
