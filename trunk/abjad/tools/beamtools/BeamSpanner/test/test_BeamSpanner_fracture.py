from abjad import *


def test_BeamSpanner_fracture_01():
    '''This test shows that fracturing beyond the first leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")
    beamtools.BeamSpanner(staff[:4])
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1

    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    assert old.components == tuple(staff[:4])

    old.fracture(0, direction=Left)
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1


def test_BeamSpanner_fracture_02():

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:4])
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1

    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    assert old.components == tuple(staff[:4])

    old.fracture(1, direction=Left)
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 2


def test_BeamSpanner_fracture_03():
    '''This test shows that fracurting beyond the last leaf
    effectively does nothing except to replace an existing
    spanner with an identical new spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:4])
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1

    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    assert old.components == tuple(staff[:4])

    old.fracture(-1, direction=Right)
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1


def test_BeamSpanner_fracture_04():

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:4])
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 1

    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    assert old.components == tuple(staff[:4])

    old.fracture(1, direction=Right)
    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 2


def test_BeamSpanner_fracture_05():
    '''Fracture both sides of leaf.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:5])
    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    old.fracture(2, direction=None)

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

    assert len(beamtools.get_beam_spanner_attached_to_component(staff[0])) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[2])) == 1
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[3])) == 2

    assert beamtools.get_beam_spanner_attached_to_component(staff[0]) != \
        beamtools.get_beam_spanner_attached_to_component(staff[2])
    assert beamtools.get_beam_spanner_attached_to_component(staff[2]) != \
        beamtools.get_beam_spanner_attached_to_component(staff[3])

    wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8 ]\n\td'8 [ ]\n\tef'8 [\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"



def test_BeamSpanner_fracture_06():
    '''Fracture both sides of first leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:5])
    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    old.fracture(0, direction=None)

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

    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 2

    assert len(beamtools.get_beam_spanner_attached_to_component(staff[0])) == 1
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[1])) == 4
    assert beamtools.get_beam_spanner_attached_to_component(staff[0]) != \
        beamtools.get_beam_spanner_attached_to_component(staff[1])

    wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8 [\n\td'8\n\tef'8\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"



def test_BeamSpanner_fracture_07():
    '''Fracture both sides of last leaf in spanner.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:5])
    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    old.fracture(4, direction=None)

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

    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[0])) == 4
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[4])) == 1
    assert beamtools.get_beam_spanner_attached_to_component(staff[0]) != \
        beamtools.get_beam_spanner_attached_to_component(staff[4])

    wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"



def test_BeamSpanner_fracture_08():
    '''Fracture both sides of leaf with negative index.
    '''

    staff = Staff("c'8 cs'8 d'8 ef'8 e'8 f'8 fs'8 g'8")
    beamtools.BeamSpanner(staff[:5])
    old = list(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff))[0]
    old.fracture(-1, direction=None)

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

    assert len(
        spannertools.get_spanners_attached_to_any_improper_child_of_component(
        staff)) == 2
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[0])) == 4
    assert len(beamtools.get_beam_spanner_attached_to_component(staff[4])) == 1
    assert beamtools.get_beam_spanner_attached_to_component(staff[0]) != \
        beamtools.get_beam_spanner_attached_to_component(staff[4])

    wellformednesstools.is_well_formed_component(staff)
    assert staff.lilypond_format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"
