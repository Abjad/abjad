def get_proper_contents_of_component(component):
    r'''.. versionadded:: 2.9

    Get proper contents of `component`::

        >>> staff = Staff("c' d' e' f'")

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> componenttools.get_proper_contents_of_component(staff)
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

    The function works on leaves::

        >>> componenttools.get_proper_contents_of_component(staff[0])
        []

    Return list of the proper contents of component.
    '''

    return list(getattr(component, 'music', []))
