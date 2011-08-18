from abjad.tools.containertools.Container import Container


def delete_contents_of_container(container):
    r'''Delete contents of `container`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> spannertools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8, e'8, f'8)

    ::

        abjad> f(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
        }

    ::

        abjad> containertools.delete_contents_of_container(staff)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    ::

        abjad> f(staff)
        \new Staff {
        }

    Return `container` contents.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_delete()`` to
        ``containertools.delete_contents_of_container()``.
    '''

    if not isinstance(container, Container):
        raise TypeError('must be container.')

    contents = container[:]
    del(container[:])

    return contents
