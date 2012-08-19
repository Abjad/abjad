def get_first_instance_of_klass_in_proper_parentage_of_component(component, klass):
    '''.. versionadded:: 1.1

    Get first instance of `klass` in proper parentage of `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> componenttools.get_first_instance_of_klass_in_proper_parentage_of_component(
        ...     staff[0], Staff)
        Staff{4}

    Return component or none.

    .. versionchanged:: 2.0
        renamed ``componenttools.get_first()`` to
        ``componenttools.get_first_instance_of_klass_in_proper_parentage_of_component()``.
    '''
    from abjad.tools import componenttools

    for parent in componenttools.get_proper_parentage_of_component(component):
        if isinstance(parent, klass):
            return parent
