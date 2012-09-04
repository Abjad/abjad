def get_clef_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get clef marks attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> contexttools.get_clef_marks_attached_to_component(staff)
        (ClefMark('treble')(Staff{4}),)

    Return tuple of zero or more clef marks.
    '''
    from abjad.tools import contexttools

    return contexttools.get_context_marks_attached_to_component(component, klasses=(contexttools.ClefMark,))
