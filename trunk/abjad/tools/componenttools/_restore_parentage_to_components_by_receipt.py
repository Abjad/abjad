def _restore_parentage_to_components_by_receipt(receipt):
    '''Restore parentage to components by receipt.

    Use after call to _set_component_parents_to_none(components).

    Return none.
    '''

    for component, parent in receipt:
        assert component._parent is None
        component._switch(parent)
