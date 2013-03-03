from abjad.tools import durationtools
from abjad.tools import selectiontools


def all_are_components_scalable_by_multiplier(components, multiplier):
    '''.. versionadded:: 1.1

    True when `components` are all scalable by `multiplier`::

        >>> components = [Note(0, (1, 8))]
        >>> componenttools.all_are_components_scalable_by_multiplier(components, Multiplier(3, 2))
        True

    Otherwise false::

        >>> components = [Note(0, (1, 8))]
        >>> componenttools.all_are_components_scalable_by_multiplier(components, Multiplier(2, 3))
        False

    Return boolean.
    '''
    from abjad.tools import leaftools

    # check input
    multiplier = durationtools.Multiplier(multiplier)

    # check components
    for component in components:
        if isinstance(component, leaftools.Leaf):
            candidate_duration = multiplier * component.written_duration
            if not candidate_duration.is_assignable:
                return False

    return True
