from abjad.tools import componenttools


def is_component_with_articulation_attached(expr, articulation_name=None):
    '''.. versionadded:: 2.3

    True when `expr` is component with articulation attached::

        >>> note = Note("c'4")
        >>> marktools.Articulation('staccato')(note)
        Articulation('staccato')(c'4)

    ::

        >>> marktools.is_component_with_articulation_attached(note)
        True

    False otherwise::

        >>> note = Note("c'4")

    ::

        >>> marktools.is_component_with_articulation_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools import marktools

    if isinstance(expr, componenttools.Component):
        for articulation in marktools.get_articulations_attached_to_component(expr):
            if articulation.name == articulation_name or articulation_name is None:
                return True

    return False
