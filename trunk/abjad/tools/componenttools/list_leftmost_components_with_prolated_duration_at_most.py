from abjad.tools import durationtools


def list_leftmost_components_with_prolated_duration_at_most(components, prolated_duration):
    '''.. versionadded:: 2.0

    List leftmost components in `component` with prolated duration at most `prolated_duration`.

    Return tuple of ``components[:i]`` together with the prolated duration of ``components[:i]``::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> componenttools.list_leftmost_components_with_prolated_duration_at_most(voice[:], Duration(1, 4))
        ([Note("c'8"), Note("d'8")], Duration(1, 4))

    Maximize ``i`` such that the prolated duration of
    ``components[:i]`` is no greater than `prolated_duration`.

    Input `components` must be thread-contiguous.

    .. todo:: implement
        ``componenttools.list_leftmost_components_with_prolated_duration_at_least()``.

    .. todo:: implement
        ``componenttools.list_rightmost_components_with_prolated_duration_at_most()``.

    .. todo:: implement
        ``componenttools.list_rightmost_components_with_prolated_duration_at_least()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.get_le_duration_prolated()`` to
        ``componenttools.list_leftmost_components_with_prolated_duration_at_most()``.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(components)

    total_duration = durationtools.Duration(0)
    result = []
    for component in components:
        cur_duration = component.prolated_duration
        if total_duration + cur_duration <= prolated_duration:
            result.append(component)
            total_duration += cur_duration
        else:
            break

    return result, total_duration
