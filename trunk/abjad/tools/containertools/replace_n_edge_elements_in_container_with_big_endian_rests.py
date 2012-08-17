def replace_n_edge_elements_in_container_with_big_endian_rests(container, n):
    r'''.. versionadded:: 2.0

    .. note:: Deprecated. Use ``containertools.replace_container_slice_with_rests()`` instead.

    Replace `n` edge elements in `container` with big-endian rests::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }

    ::

        >>> containertools.replace_n_edge_elements_in_container_with_big_endian_rests(staff, -5)
        Staff{3}

    ::

        >>> f(staff)
        \new Staff {
            c'8
            r2
            r8
        }

    Return `container`.

    .. versionchanged:: 2.0
        renamed ``containertools.replace_first_n_elements_in_container_with_big_endian_rests()`` to
        ``containertools.replace_n_edge_elements_in_container_with_big_endian_rests()``.
    '''
    from abjad.tools import containertools

    if 0 <= n:
        return containertools.replace_container_slice_with_rests(container, stop=n, big_endian=True)
    else:
        return containertools.replace_container_slice_with_rests(container, start=n, big_endian=True)
