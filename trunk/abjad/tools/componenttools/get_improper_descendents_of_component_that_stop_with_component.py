def get_improper_descendents_of_component_that_stop_with_component(component):
    r'''.. versionadded:: 2.9

    Get improper descendents of `component` that stop with `component`::

        >>> staff = Staff(r"c' << \new Voice { d' } \new Voice { e' } >> f'")

    ::

        >>> f(staff)
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

        >>> componenttools.get_improper_descendents_of_component_that_stop_with_component(staff)
        [Staff{3}, Note("f'4")]

    Return list of `component` together with proper contents that stop with `component`.

    .. versionchanged:: 2.9
        renamed ``componenttools.get_improper_contents_of_component_that_stop_with_component()`` to
        ``componenttools.get_improper_descendents_of_component_that_stop_with_component()``.
    '''
    from abjad.tools import containertools

    # initialize result
    result = []

    # add component
    result.append(component)

    # add proper contents that stop with component
    if isinstance(component, containertools.Container):
        if component.is_parallel:
            duration = component.preprolated_duration
            for x in component:
                if x.preprolated_duration == duration:
                    result.extend(get_improper_descendents_of_component_that_stop_with_component(x))
        elif component:
            result.extend(get_improper_descendents_of_component_that_stop_with_component(component[-1]))

    # return result
    return result
