# -*- encoding: utf-8 -*-
def eject_contents_of_container(container):
    '''Eject contents of `container`:

    ::

        >>> container = Container("c'8 d'8 e'8 f'8")

    ..  doctest::

        >>> f(container)
        {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> containertools.eject_contents_of_container(container)
        SliceSelection(Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"))

    ::

        >>> container
        {}

    ..  doctest::

        >>> f(container)
        {
        }

    Return list of `container` contents.
    '''
    from abjad.tools import containertools

    contents = container[:]
    containertools.delete_contents_of_container(container)

    return contents
