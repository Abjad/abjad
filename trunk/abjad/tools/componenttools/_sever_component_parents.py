# TODO: eventually implement as private method bound to selection
def _sever_component_parents(components):
    '''No contiguity requirements.
    Return receipt of unordered set of (component, parent) pairs.
    Use to temporarily detach components from screo tree.
    Then do some other operation, probably copy.
    Then call _componenttools._restore_component_parents().
    '''
    from abjad.tools import componenttools
    assert componenttools.all_are_components(components)
    receipt = set([])
    for component in components:
        receipt.add(component._sever_parent())
    return receipt
