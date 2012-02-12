from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent
from abjad.tools.componenttools.get_parent_and_start_stop_indices_of_components import get_parent_and_start_stop_indices_of_components


def _give_donor_components_position_in_parent_to_recipient_components(donors, recipients):
    '''When 'donors' has a parent, find parent.
        Then insert all components in 'recipients'
        in parent immediately before 'donors'.
        Then remove 'donors' from parent.

        When 'donors' has no parent, do nothing.

        Return 'donors'.

        Helper implements no spanner-handling at all.
        Helper is not composer-safe and may cause discontiguous spanners.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_contiguous_components_in_same_parent(donors)
    assert componenttools.all_are_components(recipients)

    parent, start, stop = get_parent_and_start_stop_indices_of_components(donors)

    if parent is None:
        return donors

    # to avoid pychecker slice assignment error
    #parent._music[start:start] = recipients
    parent._music.__setitem__(slice(start, start), recipients)
    _switch_components_to_parent(recipients, parent)
    _switch_components_to_parent(donors, None)

    return donors
