def get_improper_parentage_of_component(component):
    '''.. versionadded:: 1.1

    Get improper parentage of `component`::

        >>> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> note = staff.leaves[0]

    ::

        >>> componenttools.get_improper_parentage_of_component(note)
        (Note("c'8"), Tuplet(2/3, [c'8, d'8, e'8]), Staff{1})

    Return tuple of zero or more components.
    '''

    result = []
    parent = component
    while parent is not None:
        if parent in result:
            raise ContainmentError('Component is a member of its own proper parentage.')
        result.append(parent)
        parent = parent._parent
    result = tuple(result)
    return result
