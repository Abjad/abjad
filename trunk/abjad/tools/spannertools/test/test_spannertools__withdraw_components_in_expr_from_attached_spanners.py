from abjad import *
from abjad.tools.spannertools._withdraw_components_in_expr_from_attached_spanners import _withdraw_components_in_expr_from_attached_spanners


def test_spannertools__withdraw_components_in_expr_from_attached_spanners_01():
    '''Unspan every component in components.
        Navigate down into components and traverse deeply.'''

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t)
    spannertools.CrescendoSpanner(t[:])

    _withdraw_components_in_expr_from_attached_spanners([t])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_spannertools__withdraw_components_in_expr_from_attached_spanners_02():
    '''Docs.'''

    t = Staff(Container(notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BeamSpanner(t.leaves[:3])
    spannertools.BeamSpanner(t.leaves[3:])

    r'''
    \new Staff {
        {
            c'8 [
            d'8
        }
        {
            e'8 ]
            f'8 [
        }
        {
            g'8
            a'8 ]
        }
    }
    '''

    _withdraw_components_in_expr_from_attached_spanners([t[1]])

    r'''
    \new Staff {
        {
            c'8 [
            d'8 ]
        }
        {
            e'8
            f'8
        }
        {
            g'8 [
            a'8 ]
        }
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"
