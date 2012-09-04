def get_time_signature_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get time signature mark attached to `component`::

        >>> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

    ::

        >>> f(measure)
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_time_signature_mark_attached_to_component(measure)
        TimeSignatureMark((4, 8))(|4/8, c'8, d'8, e'8, f'8|)

    Return time signature mark.

    Raise missing mark error when no time signature mark attaches to `component`.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_mark_attached_to_component(
        component, klasses=(contexttools.TimeSignatureMark,))
