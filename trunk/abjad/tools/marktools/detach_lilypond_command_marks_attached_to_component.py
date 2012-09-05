def detach_lilypond_command_marks_attached_to_component(component, command_name=None):
    r'''.. versionadded:: 2.0

    Detach LilyPond command marks attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> marktools.LilyPondCommandMark('slurDotted')(staff[0])
        LilyPondCommandMark('slurDotted')(c'8)
        >>> marktools.LilyPondCommandMark('slurUp')(staff[0])
        LilyPondCommandMark('slurUp')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            \slurDotted
            \slurUp
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> marktools.detach_lilypond_command_marks_attached_to_component(staff[0])
        (LilyPondCommandMark('slurDotted'), LilyPondCommandMark('slurUp'))

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    Return tuple of zero or more marks detached.
    '''
    from abjad.tools import marktools

    marks = []
    for mark in marktools.get_lilypond_command_marks_attached_to_component(
        component, command_name = command_name):
        mark.detach()
        marks.append(mark)
    return tuple(marks)
