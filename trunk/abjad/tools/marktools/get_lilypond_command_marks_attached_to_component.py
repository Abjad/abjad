def get_lilypond_command_marks_attached_to_component(component, command_name=None):
    r'''.. versionadded:: 2.0

    Get LilyPond command marks attached to `component`::

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

        >>> marktools.get_lilypond_command_marks_attached_to_component(staff[0])
        (LilyPondCommandMark('slurDotted')(c'8), LilyPondCommandMark('slurUp')(c'8))

    Return tuple of zero or more marks.
    '''
    from abjad.tools import marktools

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, marktools.LilyPondCommandMark):
            if mark.command_name == command_name or command_name is None:
                result.append(mark)

    result = tuple(result)
    return result
