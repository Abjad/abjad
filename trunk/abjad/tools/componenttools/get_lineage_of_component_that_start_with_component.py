def get_lineage_of_component_that_start_with_component(component):
    r'''.. versionadded:: 2.9

    Get lineage of `component` that start with `component`::

        >>> staff = Staff(r"c' << \new Voice { d'8 e'8 } \new Voice { d''8 e''8 } >> f'4")

    ::

        >>> f(staff)
        \new Staff {
            c'4
            <<
                \new Voice {
                    d'8
                    e'8
                }
                \new Voice {
                    d''8
                    e''8
                }
            >>
            f'4
        }

    ::

        >>> staff[1][0]
        Voice{2}

    ::

        >>> componenttools.get_lineage_of_component_that_start_with_component(staff[1][0])
        [<<Voice{2}, Voice{2}>>, Voice{2}, Note("d'8")]

    Return list of all components in the lineage of `component` that
    start with `component`.

    The list always includes `component`.
    '''
    from abjad.tools import componenttools

    # initialize result
    result = []
    
    result.extend(componenttools.get_improper_parentage_of_component_that_start_with_component(component))

    result.remove(component)

    result.extend(componenttools.get_improper_descendents_of_component_that_start_with_component(component))

    return result
