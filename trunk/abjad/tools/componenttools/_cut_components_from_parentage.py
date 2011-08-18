def _cut_components_from_parentage(components):
    '''Cut all components in list from parent.

    Does not handle spanners and so not composer-safe.

    Return components.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_components(components)

    for component in components:
        component._parentage._cut()

    return components
