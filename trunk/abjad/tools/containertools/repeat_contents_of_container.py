def repeat_contents_of_container(container, total=2):
    r'''.. versionadded:: 1.1

    Repeat contents of `container`::

        >>> staff = Staff("c'8 d'8")
        >>> beamtools.BeamSpanner(staff.leaves)
        BeamSpanner(c'8, d'8)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
        }

    ::

        >>> containertools.repeat_contents_of_container(staff, 3)
        Staff{6}

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
            c'8 [
            d'8 ]
            c'8 [
            d'8 ]
        }

    Leave `container` unchanged when `total` is ``1``.

    Empty `container` when `total` is ``0``.

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.contents_multiply()`` to
        ``containertools.repeat_contents_of_container()``.
    '''
    from abjad.tools import containertools

    if not isinstance(container, containertools.Container):
        raise TypeError('must be container: %s' % container)

    if not isinstance(total, int):
        raise TypeError('must be int: %s' % total)

    if not 0 <= total:
        raise ValueError('must be greater than or equal to zero: %s' % total)

    # empty container when total is zero
    if total == 0:
        # to avoid pychecker slice assignment error
        #del(container[:])
        container.__delitem__(slice(0, len(container)))
        return container

    # reproduce container contents when total is greater than zero
    n = len(container)
    return containertools.repeat_last_n_elements_of_container(container, n=n, total=total)
