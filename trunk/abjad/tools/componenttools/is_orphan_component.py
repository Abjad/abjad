def is_orphan_component(component):
    '''.. versionadded:: 1.1

    True when `component` has no parent. Otherwise false::

        >>> note = Note("c'4")
        >>> componenttools.is_orphan_component(note)
        True

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``componenttools.component_is_orphan()`` to
        ``componenttools.is_orphan_component()``.
    '''
    from abjad.tools import componenttools

    return not componenttools.get_proper_parentage_of_component(component)
