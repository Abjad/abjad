def get_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get all marks attached to `component`'::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> comment_mark = marktools.LilyPondComment('beginning of note content')(staff[0])
        >>> marktools.LilyPondCommandMark('slurDotted')(staff[0])
        LilyPondCommandMark('slurDotted')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }


    ::

        >>> marktools.get_marks_attached_to_component(staff[0])
        (LilyPondComment('beginning of note content')(c'8), LilyPondCommandMark('slurDotted')(c'8))

    Return tuple of zero or more marks.
    '''

    marks = component._marks_for_which_component_functions_as_start_component
    marks = tuple(marks)

    return marks
