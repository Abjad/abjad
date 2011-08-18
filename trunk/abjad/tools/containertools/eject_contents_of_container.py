from abjad.tools.containertools.delete_contents_of_container import delete_contents_of_container


def eject_contents_of_container(container):
    '''.. versionadded:: 2.0

    Eject contents of `container`::

        abjad> container = Container("c'8 d'8 e'8 f'8")

    ::

        abjad> f(container)
        {
            c'8
            d'8
            e'8
            f'8
        }

    ::

        abjad> containertools.eject_contents_of_container(container)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    ::

        abjad> container
        {}

    ::

        abjad> f(container)
        {
        }

    Return list of `container` contents.
    '''

    contents = container[:]
    delete_contents_of_container(container)

    return contents
