# TODO: eventually implement as private method bound to selection
def _set_component_parents_to_none(components):
    '''No contiguity requirements.
    Use to temporarily 'lift' parent references.
    Return receipt of unordered set of (component, parent) pairs.
    Then do some other operation, probably copy.
    Then call _componenttools._restore_parentage_to_components_by_receipt().
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_components(components)

    receipt = set([])
    for component in components:
        receipt.add(component._set_parent_to_none())

    return receipt
