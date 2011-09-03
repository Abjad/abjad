def _ignore_parentage_of_components(components):
    '''No contiguity requirements.
        Use to temporarily 'lift' parent references.
        Return receipt of unordered set of (component, parent) pairs.
        Then do some other operation, probably copy.
        Then reapply parent references.
        Call _componenttools.restore(receipt).
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_components(components)

    receipt = set([])
    for component in components:
        parent = component._parentage.parent
        component._parentage._ignore()
        receipt.add((component, parent))

    return receipt
