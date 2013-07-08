from abjad.tools import componenttools


def _withdraw_components_from_attached_spanners(components):
    '''Withdraw `components` from attached spanners.

    Unspan every component in `components`.
    Does not navigate down into components; traverse shallowly.
    Return `components`.

    Not composer-safe.
    '''

    # check input
    assert componenttools.all_are_components(components)

    # withdraw components
    for component in components:
        for spanner in component.spanners:
            spanner._remove(component)

    # return components
    return components
