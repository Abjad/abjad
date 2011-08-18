from abjad import *
from abjad.tools.componenttools._give_donor_components_position_in_parent_to_recipient_components import _give_donor_components_position_in_parent_to_recipient_components


def test_componenttools__give_donor_components_position_in_parent_to_recipient_components_01():
    '''Not composer-safe.'''

    t = Voice("c'8 d'8 e'8 f'8")
    spannertools.BeamSpanner(t[:])
    notes = [Note("c'16"), Note("d'16")]

    _give_donor_components_position_in_parent_to_recipient_components(t[0:1], notes)

    "Container t is now ..."

    r'''
    \new Voice {
        c'16
        d'16
        d'8
        e'8
        f'8 ]
    }
    '''

    assert t.format == "\\new Voice {\n\tc'16\n\td'16\n\td'8\n\te'8\n\tf'8 ]\n}"

    "Container t now carries a discontiguous spanner."

    assert not componenttools.is_well_formed_component(t)
