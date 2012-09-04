def get_context_mark_attached_to_component(component, klasses=None):
    r'''.. versionadded:: 2.3

    Get context mark attached to `component`::

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

        >>> contexttools.get_context_mark_attached_to_component(staff)
        ClefMark('treble')(Staff{4})

    Return context mark.

    Raise missing mark error when no context mark attaches to `component`.
    '''
    from abjad.tools import contexttools

    if klasses is None:
        klasses = (contexttools.ContextMark,)

    context_marks = contexttools.get_context_marks_attached_to_component(component, klasses=klasses)

    if len(context_marks) == 0:
        raise MissingMarkError
    elif 1 < len(context_marks):
        raise ExtraMarkError
    else:
        return context_marks[0]
