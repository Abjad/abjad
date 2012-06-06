def get_improper_contents_of_component(component):
    r'''.. versionadded:: 2.9

    Get improper contents of `component`::

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

        >>> componenttools.get_improper_contents_of_component(staff)
        [Staff{4}, Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4")]

    The functions works for both containers and leaves.

    Return a list of `component` together with the proper contents of `component`.
    '''

    # initialize result
    result = []

    # append component
    result.append(component)

    # extend proper contents of component
    result.extend(getattr(component, 'music', []))

    # return result
    return result
