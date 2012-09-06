def get_down_markup_attached_to_component(component):
    '''.. versionadded:: 2.0

    Get down-markup attached to component::

        >>> chord = Chord([-11, 2, 5], (1, 4))

    ::

        >>> markuptools.Markup('UP', Up)(chord)
        Markup(('UP',), direction=Up)(<cs d' f'>4)

    ::

        >>> markuptools.Markup('DOWN', Down)(chord)
        Markup(('DOWN',), direction=Down)(<cs d' f'>4)

    ::

        >>> markuptools.get_down_markup_attached_to_component(chord)
        (Markup(('DOWN',), direction=Down)(<cs d' f'>4),)

    Return tuple of zero or more markup objects.
    '''
    from abjad.tools import markuptools

    result = []

    markups = markuptools.get_markup_attached_to_component(component)
    for markup in markups:
        if markup.direction is Down:
            result.append(markup)

    return tuple(result)
