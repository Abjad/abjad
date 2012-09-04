def _switch_components_to_parent(components, parent):
    '''Switch components to parent.

    Not composer-safe.

    Return components.
    '''
    from abjad.tools import componenttools

    if not componenttools.all_are_thread_contiguous_components(components):
        raise TypeError('can not switch parent of "%s".' % str(components))

    for component in components:
        component._switch(parent)

    return components
