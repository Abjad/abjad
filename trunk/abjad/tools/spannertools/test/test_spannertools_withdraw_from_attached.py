from abjad import *
from abjad.tools.spannertools._withdraw_components_from_attached_spanners import _withdraw_components_from_attached_spanners


def test_spannertools_withdraw_from_attached_01():
    t = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(t[:])
    _withdraw_components_from_attached_spanners(t[:])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spannertools_withdraw_from_attached_02():
    t = Staff("c'8 d'8 e'8 f'8")
    beamtools.BeamSpanner(t[:])
    _withdraw_components_from_attached_spanners(t[0:2])

    r'''
    \new Staff {
        c'8
        d'8
        e'8 [
        f'8 ]
    }
    '''

    assert wellformednesstools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8\n\td'8\n\te'8 [\n\tf'8 ]\n}"


def test_spannertools_withdraw_from_attached_03():
    t = _withdraw_components_from_attached_spanners([])
    assert t == []
