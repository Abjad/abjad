from abjad.tools import durationtools


def all_are_components_scalable_by_multiplier(components, multiplier):
    '''.. versionadded:: 1.1

    True when `components` are all scalable by `multiplier`::

        >>> components = [Note(0, (1, 8))]
        >>> componenttools.all_are_components_scalable_by_multiplier(components, Duration(3, 2))
        True

    Otherwise false::

        >>> components = [Note(0, (1, 8))]
        >>> componenttools.all_are_components_scalable_by_multiplier(components, Duration(2, 3))
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``durationtools.are_scalable()`` to
        ``componenttools.all_are_components_scalable_by_multiplier()``.
    '''
    from abjad.tools import leaftools

    for component in components:
        if isinstance(component, leaftools.Leaf):
            candidate_duration = multiplier * component.written_duration
            if not durationtools.is_assignable_rational(candidate_duration):
                return False

    return True
