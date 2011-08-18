from abjad.tools.containertools._replace_first_n_elements_in_container_with_rests import _replace_first_n_elements_in_container_with_rests


def replace_n_edge_elements_in_container_with_big_endian_rests(container, n):
    r'''.. versionadded:: 2.0

    Replace `n` edge elements in `container` with big-endian rests::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
        }

    ::

        abjad> containertools.replace_n_edge_elements_in_container_with_big_endian_rests(staff, -5)
        Staff{3}

    ::

        abjad> f(staff)
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

    if 0 <= n:
        rested_half = 'left'
    else:
        rested_half = 'right'

    return _replace_first_n_elements_in_container_with_rests(container, n, rested_half, 'big-endian')
