def get_lineage_of_component_that_stop_with_component(component):
    r'''.. versionadded:: 2.9

    Get lineage of `component` that stop with `component`::

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

        >>> componenttools.get_lineage_of_component_that_stop_with_component(staff[1][0])
        [<<Voice{2}, Voice{2}>>, Voice{2}, Note("e'8")]

    Return list of all components in the lineage of `component` that
    stop with `component`.

    The list always includes `component`.
    '''
    from abjad.tools import componenttools

    # initialize result
    result = []
    
    # add parentage of component that start with component
    result.extend(componenttools.get_improper_parentage_of_component_that_stop_with_component(component))

    # remove component
    result.remove(component)

    # component and descendents of component that start with component
    result.extend(componenttools.get_improper_descendents_of_component_that_stop_with_component(component))

    # return result
    return result
