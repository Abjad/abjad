def get_most_distant_sequential_container_in_improper_parentage_of_component(component):
    r'''.. versionadded:: 2.9

    Get first sequential container in the improper parentage of `component`
    such that the parent of sequential container is either a parellel container
    or else none::

        >>> voice_1 = Voice("c'8 d'8")
        >>> voice_2 = Voice("e'8 f'8")
        >>> t = Voice([Container([voice_1, voice_2])])
        >>> t[0].is_parallel = True
        >>> t[0][0].name = 'voice 1'
        >>> t[0][1].name = 'voice 2'

    ::

        >>> f(t)
        \new Voice {
            <<
                \context Voice = "voice 1" {
                    c'8
                    d'8
                }
                \context Voice = "voice 2" {
                    e'8
                    f'8
                }
            >>
        }

    ::

        >>> note = t.leaves[1]

    ::

        >>> componenttools.get_most_distant_sequential_container_in_improper_parentage_of_component(
        ...     note) 
        Voice-"voice 1"{2}

    Return none when no such container exists in the improper parentage of `component`.
    '''
    from abjad.tools import containertools
    from abjad.tools import componenttools

    for component in componenttools.get_improper_parentage_of_component(component):
        if isinstance(component, containertools.Container) and not component.is_parallel:
            if component.parent is None:
                return component
            if isinstance(component.parent, containertools.Container) and \
                component.parent.is_parallel:
                return component
