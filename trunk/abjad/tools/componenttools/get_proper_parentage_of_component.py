def get_proper_parentage_of_component(component):
    '''.. versionadded:: 1.1

    Get proper parentage of `component`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> note = staff.leaves[0]
        >>> componenttools.get_proper_parentage_of_component(note)
        (FixedDurationTuplet(1/4, [c'8, d'8, e'8]), Staff{1})

    Return tuple of zero or more components.
    '''
    from abjad.tools import componenttools

    return componenttools.get_improper_parentage_of_component(component)[1:]
