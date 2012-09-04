def eject_contents_of_container(container):
    '''.. versionadded:: 2.0

    Eject contents of `container`::

        >>> container = Container("c'8 d'8 e'8 f'8")

    ::

        >>> f(container)
        {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> containertools.eject_contents_of_container(container)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    ::

        >>> container
        {}

    ::

        >>> f(container)
        {
        }

    Return list of `container` contents.
    '''
    from abjad.tools import containertools

    contents = container[:]
    containertools.delete_contents_of_container(container)

    return contents
