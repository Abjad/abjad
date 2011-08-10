def _restore_parentage_to_components_by_receipt(receipt):
    '''Restore parentage to components by receipt.

    Use after call to _ignore_parentage_of_components(components).

    Return none.
    '''

    for component, parent in receipt:
        assert component._parentage.parent is None
        component._parentage._switch(parent)
