from abjad.tools.marktools.get_lilypond_comments_attached_to_component import get_lilypond_comments_attached_to_component


def detach_lilypond_comments_attached_to_component(component):
    r'''.. versionadded:: 2.0

    Detach LilyPond comments attached to `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> slur = spannertools.SlurSpanner(staff.leaves)
        abjad> marktools.LilyPondComment('comment 1')(staff[0])
        LilyPondComment('comment 1')(c'8)
        abjad> marktools.LilyPondComment('comment 2')(staff[0])
        LilyPondComment('comment 2')(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            % comment 1
            % comment 2
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> marktools.detach_lilypond_comments_attached_to_component(staff[0])
        (LilyPondComment('comment 1'), LilyPondComment('comment 2'))

    ::

        abjad> f(staff)
        \new Staff {
            c'8 (
            d'8
            e'8
            f'8 )
        }

    ::

        abjad> marktools.get_lilypond_comments_attached_to_component(staff[0])
        ()

    Return tuple or zero or more LilyPond comments.
    '''

    comments = []
    for comment in get_lilypond_comments_attached_to_component(component):
        comment.detach()
        comments.append(comment)

    return tuple(comments)
