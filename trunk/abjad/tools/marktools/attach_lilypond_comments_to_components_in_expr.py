def attach_lilypond_comments_to_components_in_expr(expr, lilypond_comments):
    r'''.. versionadded:: 2.3

    Attach `lilypond_comments` to components in `expr`::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_comment = marktools.LilyPondComment('foo', 'right')
        >>> marktools.attach_lilypond_comments_to_components_in_expr(
        ...     staff.leaves, [lilypond_comment])

    ::

        >>> f(staff)
        \new Staff {
            c'8 % foo
            d'8 % foo
            e'8 % foo
            f'8 % foo
        }

    Return none.
    '''
    from abjad.tools import iterationtools
    from abjad.tools import marktools

    for component in iterationtools.iterate_components_in_expr(expr):
        for lilypond_comment in lilypond_comments:
            marktools.LilyPondComment(lilypond_comment)(component)
