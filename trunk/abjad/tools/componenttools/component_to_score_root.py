def component_to_score_root(component):
    '''.. versionadded:: 1.1

    Change `component` to score root::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")
        >>> staff = Staff([tuplet])
        >>> note = staff.leaves[0]
        >>> componenttools.component_to_score_root(note)
        Staff{1}

    Return score root.
    '''
    from abjad.tools import componenttools

    return componenttools.get_improper_parentage_of_component(component)[-1]
