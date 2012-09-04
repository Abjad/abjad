def component_to_score_depth(component):
    '''.. versionadded:: 1.1

    Change `component` to score depth::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> componenttools.component_to_score_depth(staff.leaves[0])
        2

    Return nonnegative integer.
    '''
    from abjad.tools import componenttools

    return len(componenttools.get_proper_parentage_of_component(component))
