def _set_component_parents(components, parent):
    '''Set component parents.
    Not composer-safe.
    Return components.
    '''
    from abjad.tools import componenttools
    if not componenttools.all_are_thread_contiguous_components(components):
        message = 'can not set {!r} parent.'
        raise TypeError(message.format(components))
    for component in components:
        component._set_parent(parent)
    return components
