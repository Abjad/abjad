def delete_contents_of_container(container):
    r'''Delete contents of `container`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> containertools.delete_contents_of_container(staff)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    ::

        >>> f(staff)
        \new Staff {
        }

    Return `container` contents.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_delete()`` to
        ``containertools.delete_contents_of_container()``.
    '''
    from abjad.tools import containertools

    if not isinstance(container, containertools.Container):
        raise TypeError('must be container.')

    contents = container[:]
    # to avoid pychecker slice assignment error
    #del(container[:])
    container.__delitem__(slice(0, len(container)))

    return contents
