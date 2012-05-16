def get_improper_contents_of_component_that_stop_with_component(component):
    r'''.. versionadded:: 2.9

    Get improper contents of `component` that stop with `component`::

        abjad> staff = Staff(r"c' << \new Voice { d' } \new Voice { e' } >> f'")

    ::

        abjad> f(staff)
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

        abjad> componenttools.get_improper_contents_of_component_that_stop_with_component(staff)
        [Staff{3}, Note("f'4")]

    Return list of `component` together with proper contents that stop with `component`.
    '''
    from abjad.tools.containertools.Container import Container

    # initialize result
    result = []

    # add component
    result.append(component)

    # add proper contents that stop with component
    if isinstance(component, Container):
        if component.is_parallel:
            duration = component.preprolated_duration
            for x in component:
                if x.preprolated_duration == duration:
                    result.extend(get_improper_contents_of_component_that_stop_with_component(x))
        elif component:
            result.extend(get_improper_contents_of_component_that_stop_with_component(component[-1]))

    # return result
    return result
