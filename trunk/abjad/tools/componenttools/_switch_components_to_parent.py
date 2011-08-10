from abjad.tools.componenttools.all_are_thread_contiguous_components import all_are_thread_contiguous_components


def _switch_components_to_parent(components, parent):
    '''Switch components to parent.

    Not composer-safe.

    Return components.
    '''

    if not all_are_thread_contiguous_components(components):
        raise TypeError('can not switch parent of "%s".' % str(components))

    for component in components:
        component._parentage._switch(parent)

    return components
