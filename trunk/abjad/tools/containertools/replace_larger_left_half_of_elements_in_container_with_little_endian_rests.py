from abjad.tools.containertools._replace_half_of_elements_in_container_with_rests import _replace_half_of_elements_in_container_with_rests


def replace_larger_left_half_of_elements_in_container_with_little_endian_rests(container):
    r'''.. versionadded:: 2.0

    Replace larger left half of elements in `container` with little-endian rests::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8 d''8 e''8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
            d''8
            e''8
        }

    ::

        abjad> containertools.replace_larger_left_half_of_elements_in_container_with_little_endian_rests(staff)
        Staff{7}

    ::

        abjad> f(staff)
        \new Staff {
            r8
            r2
            a'8
            b'8
            c''8
            d''8
            e''8
        }

    Return `container`.
    '''

    return _replace_half_of_elements_in_container_with_rests(container, 'left', 'left', 'little-endian')
