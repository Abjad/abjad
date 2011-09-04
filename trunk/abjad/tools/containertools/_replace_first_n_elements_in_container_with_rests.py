from abjad.tools import durationtools


def _replace_first_n_elements_in_container_with_rests(container, i, rested_half,
    direction = 'automatic'):
    r'''Replace the `i` elements in the `rested_half` of `container` with rests::

        abjad> from abjad.tools.containertools._replace_first_n_elements_in_container_with_rests import _replace_first_n_elements_in_container_with_rests

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 5, 'left', 'automatic')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            r8
            r2
            a'8
            b'8
        }

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 5, 'left', 'big-endian')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            r2
            r8
            a'8
            b'8
        }

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 5, 'left', 'little-endian')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            r8
            r2
            a'8
            b'8
        }

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 2, 'right', 'automatic')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            r2
            r8
        }

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 2, 'right', 'big-endian')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            r2
            r8
        }

    ::

        abjad> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8")
        abjad> _replace_first_n_elements_in_container_with_rests(staff, 2, 'right', 'little-endian')
        Staff{4}
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            r8
            r2
        }

    Return `container`.

    Set `direction` to control the order of rests created.

    .. todo: replace 'left' and 'right' with positive and negative
        values of `i`.
    '''
    from abjad.tools import resttools

    # assert keyword values
    assert rested_half in ('left', 'right')

    if direction not in ('automatic', 'big-endian', 'little-endian'):
        raise ValueError('unknown direction: %s' % direction)

    # set rest chain direction based on rested part of container
    if direction == 'automatic':
        if rested_half == 'left':
            direction = 'little-endian'
        elif rested_half == 'right':
            direction = 'big-endian'

    # get elements to replace in container
    if rested_half == 'left':
        elements_to_replace = container[:i]
    elif rested_half == 'right':
        elements_to_replace = container[i:]

    # if there are elements to replace
    if elements_to_replace:

        # find preprolated duration of elements to replace
        duration = sum([x.preprolated_duration for x in elements_to_replace])

        # construct rest chain equal in preprolated duration to replace
        rests = resttools.make_rests(duration, direction)

        # replace elements in rested_half of container with rest chain
        if rested_half == 'left':
            container[:i] = rests
        else:
            container[i:] = rests

    # return container
    return container
