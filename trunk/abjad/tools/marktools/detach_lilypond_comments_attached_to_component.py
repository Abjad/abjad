def detach_lilypond_comments_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach LilyPond comments attached to `component`::

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

        >>> marktools.detach_lilypond_comments_attached_to_component(staff[0])
        (LilyPondComment('comment 1'), LilyPondComment('comment 2'))

    ::

        >>> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        >>> marktools.get_lilypond_comments_attached_to_component(staff[0])
        ()

    Return tuple or zero or more LilyPond comments.
    '''
    from abjad.tools import marktools

    comments = []
    for comment in marktools.get_lilypond_comments_attached_to_component(component):
        comment.detach()
        comments.append(comment)

    return tuple(comments)
