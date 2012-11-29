from abjad.tools import durationtools


# TODO: implement related function to shorten from right edge.
# TODO: allow large values of `prolated_duration` to empty container contents.
def shorten_component_by_prolated_duration(component, duration):
    r'''.. versionadded:: 2.0

    Shorten `component` by prolated `duration`.

    Example 1. Shorten container and produce note with dotted duration::

        >>> staff = Staff("c'8 [ d'8 e'8 f'8 ]")

    ::

        >>> componenttools.shorten_component_by_prolated_duration(staff, Duration(1, 32))

    ::

        >>> f(staff)
        \new Staff {
            c'16. [
            d'8
            e'8
            f'8 ]
        }

    ::
    
        >>> show(staff) # doctest: +SKIP

    Example 2. Shorten container and produce note with tied duration::

        >>> staff = Staff("c'8 [ d'8 e'8 f'8 ]")

    ::

        >>> componenttools.shorten_component_by_prolated_duration(staff, Duration(3, 64))

    ::

        >>> f(staff)
        \new Staff {
            c'16 [ ~
            c'64
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Example 3. Shorten container and produce note with non-power-of-two duration::

        >>> staff = Staff("c'8 [ d'8 e'8 f'8 ]")

    ::

        >>> componenttools.shorten_component_by_prolated_duration(staff, Duration(1, 24))

    ::

        >>> f(staff)
        \new Staff {
            \times 2/3 {
                c'8 [
            }
            d'8
            e'8
            f'8 ]
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return none.
    '''
    from abjad.tools import componenttools
    from abjad.tools import leaftools

    assert isinstance(component, componenttools.Component)
    duration = durationtools.Duration(duration)

    if component.prolated_duration <= duration:
        raise NegativeDurationError('component durations must be positive.')

    if isinstance(component, leaftools.Leaf):
        new_prolated_duration = component.prolated_duration - duration
        prolation = component.prolation
        new_written_duration = new_prolated_duration / prolation
        leaftools.set_preprolated_leaf_duration(component, new_written_duration)
    else:
        container = component
        components, accumulated_duration = \
            componenttools.get_leftmost_components_with_prolated_duration_at_most(container[:], duration)
        del(container[:len(components)])
        remaining_subtrahend_duration = duration - accumulated_duration
        componenttools.shorten_component_by_prolated_duration(container[0], remaining_subtrahend_duration)
