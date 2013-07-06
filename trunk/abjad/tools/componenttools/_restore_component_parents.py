def _restore_component_parents(receipt):
    '''Restore component parents.
    Use after componenttools._sever_component_parents(components).
    Not composer-safe.
    Return none.
    '''
    for component, parent in receipt:
        assert component._parent is None, repr(component)
        component._set_parent(parent)
