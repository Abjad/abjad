from abjad.tools.marktools.get_articulations_attached_to_component import get_articulations_attached_to_component


def is_component_with_articulation_attached(expr, articulation_name = None):
    '''.. versionadded:: 2.3

    True when `expr` is component with articulation attached::

        abjad> note = Note("c'4")
        abjad> marktools.Articulation('staccato')(note)
        Articulation('staccato')(c'4)

    ::

        abjad> marktools.is_component_with_articulation_attached(note)
        True

    False otherwise::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.is_component_with_articulation_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
        for articulation in get_articulations_attached_to_component(expr):
            if articulation.name == articulation_name or articulation_name is None:
                return True

    return False
