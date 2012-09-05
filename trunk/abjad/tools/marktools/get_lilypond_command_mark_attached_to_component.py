def get_lilypond_command_mark_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get exactly one LilyPond command mark attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> marktools.LilyPondCommandMark('stemUp')(staff[0])
        LilyPondCommandMark('stemUp')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            \stemUp
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> marktools.get_lilypond_command_mark_attached_to_component(staff[0])
        LilyPondCommandMark('stemUp')(c'8)

    Return one LilyPond command mark.

    Raise missing mark error when no LilyPond command mark is attached.

    Raise extra mark error when more than one LilyPond command mark is attached.
    '''
    from abjad.tools import marktools

    lilypond_command_marks = marktools.get_lilypond_command_marks_attached_to_component(component)
    if not lilypond_command_marks:
        raise MissingMarkError
    elif 1 < len(lilypond_command_marks):
        raise ExtraMarkError
    else:
        return lilypond_command_marks[0]
