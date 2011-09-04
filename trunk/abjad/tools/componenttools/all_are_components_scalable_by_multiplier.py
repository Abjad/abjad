from abjad.tools.durationtools.is_assignable_rational import is_assignable_rational


def all_are_components_scalable_by_multiplier(components, multiplier):
    '''.. versionadded:: 1.1

    True when `components` are all scalable by `multiplier`::

        abjad> components = [Note(0, (1, 8))]
        abjad> componenttools.all_are_components_scalable_by_multiplier(components, Duration(3, 2))
        True

    Otherwise false::

        abjad> components = [Note(0, (1, 8))]
        abjad> componenttools.all_are_components_scalable_by_multiplier(components, Duration(2, 3))
        False

    Return boolean.

    .. versionchanged:: 2.0
        renamed ``durationtools.are_scalable()`` to
        ``componenttools.all_are_components_scalable_by_multiplier()``.
    '''

    from abjad.tools.leaftools._Leaf import _Leaf
    for component in components:
        if isinstance(component, _Leaf):
            candidate_duration = multiplier * component.written_duration
            if not is_assignable_rational(candidate_duration):
                return False

    return True
