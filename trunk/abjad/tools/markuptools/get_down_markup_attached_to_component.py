from abjad.tools.markuptools.get_markup_attached_to_component import get_markup_attached_to_component


def get_down_markup_attached_to_component(component):
    '''.. versionadded:: 2.0

    Get down-markup attached to component::

        abjad> chord = Chord([-11, 2, 5], (1, 4))
        abjad> markuptools.Markup('UP', 'up')(chord)
        Markup('UP', '^')
        abjad> markuptools.Markup('DOWN', 'down')(chord)
        Markup('DOWN', '_')

    ::

        abjad> markuptools.get_down_markup_attached_to_component(chord)
        (Markup('DOWN', '_'),)

    Return tuple of zero or more markup objects.
    '''

    result = []

    markups = get_markup_attached_to_component(component)
    for markup in markups:
        if markup.direction == '_':
            result.append(markup)

    return tuple(result)
