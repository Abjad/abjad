from abjad.tools import componenttools
from abjad.tools import durationtools
from abjad.tools import resttools


def replace_container_slice_with_rests(container, start=None, stop=None,
    decrease_durations_monotonically=True):
    r'''.. versionadded:: 2.10

    Replace `container` slice from `start` to `stop` with rests that decrease
    durations monotonically.

    Example 1. Replace all container elements::

        >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")
    
    ::

        >>> container = containertools.replace_container_slice_with_rests(container)

        >>> f(container)
        \new Staff {
            r1
        }

    Example 2. Replace container elements from ``1`` forward::

        >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")

    ::

        >>> container = containertools.replace_container_slice_with_rests(
        ...     container, start=1)

    :: 
    
        >>> f(container)
        \new Staff {
            c'8
            r2..
        }

    Example 3. Replace container elements from ``1`` to ``2``::

        >>> container = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b' c''8")

    ::
        >>> container= containertools.replace_container_slice_with_rests(
        ...         container, start=1, stop=2)

    ::

        >>> f(container)
        \new Staff {
            c'8
            r8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }

    Return `container`.
    '''

    # get container elements to replace
    elements_to_replace = container[start:stop]
    
    # if there are elements to replace
    if elements_to_replace:

        # find preprolated duration of elements to replace
        duration = componenttools.sum_duration_of_components(
            elements_to_replace, preprolated=True)

        # construct rests equal in preprolated duration to replace
        rests = resttools.make_rests(duration,
            decrease_durations_monotonically=decrease_durations_monotonically)

        # replace container elements with rests
        container[start:stop] = rests

    # return container
    return container
