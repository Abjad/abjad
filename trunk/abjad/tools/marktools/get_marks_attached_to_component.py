def get_marks_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get all marks attached to `component`'::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> comment_mark = marktools.LilyPondComment('beginning of note content')(staff[0])
        abjad> marktools.LilyPondCommandMark('slurDotted')(staff[0])
        LilyPondCommandMark('slurDotted')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            % beginning of note content
            \slurDotted
            c'8 (
            d'8
            e'8
            f'8 )
        }


    ::

        abjad> marktools.get_marks_attached_to_component(staff[0])
        (LilyPondComment('beginning of note content')(c'8), LilyPondCommandMark('slurDotted')(c'8))

    Return tuple of zero or more marks.

    .. versionchanged:: 2.0
        renamed ``marktools.get_all_marks_attached_to_component()`` to
        ``marktools.get_marks_attached_to_component()``.
    '''

    marks = component._marks_for_which_component_functions_as_start_component
    marks = tuple(marks)

    return marks
