def get_improper_parentage_of_component_that_stop_with_component(component):
    r'''.. versionadded:: 2.9

    Get improper parentage of `component` that stop with `component`::

        >>> staff = Staff(r"c' << \new Voice { d' } \new Voice { e' } >> f'")

    ::

        f(staff)
        \new Staff {
            c'4
            <<
                \new Voice {
                    d'4
                }
                \new Voice {
                    e'4
                }
            >>
            f'4
        }

    ::

        >>> componenttools.get_improper_parentage_of_component_that_stop_with_component(
        ...     staff.leaves[-1])
        [Note("f'4"), Staff{3}]

    Return list of `component` with proper parentage that stop with `component`.
    '''
    from abjad.tools import componenttools
    
    # initialize result
    result = []

    # add component
    result.append(component)

    # add proper paretage that stop with component
    prev = component
    for parent in componenttools.get_proper_parentage_of_component(component):
        if parent.is_parallel:
            if prev.prolated_duration == parent.prolated_duration:
                result.append(parent)
            else:
                break
        elif parent.index(prev) == len(parent) - 1:
            result.append(parent)
        prev = parent

    # return result
    return result
