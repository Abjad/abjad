def get_lilypond_comments_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Get LilyPond comments attached to `component`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> slur = spannertools.SlurSpanner(staff.leaves)
        >>> marktools.LilyPondComment('comment 1')(staff[0])
        LilyPondComment('comment 1')(c'8)
        >>> marktools.LilyPondComment('comment 2')(staff[0])
        LilyPondComment('comment 2')(c'8)

    ::

        >>> f(staff)
        \new Staff {
            % comment 1
            % comment 2
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> marktools.get_lilypond_comments_attached_to_component(staff[0])
        (LilyPondComment('comment 1')(c'8), LilyPondComment('comment 2')(c'8))

    Return tuple of zero or more LilyPond comments.
    '''
    from abjad.tools import marktools

    result = []
    for mark in component._marks_for_which_component_functions_as_start_component:
        if isinstance(mark, marktools.LilyPondComment):
            result.append(mark)

    result = tuple(result)
    return result
