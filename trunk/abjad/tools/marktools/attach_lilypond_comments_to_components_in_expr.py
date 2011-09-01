from abjad.tools.marktools.LilyPondComment import LilyPondComment


def attach_lilypond_comments_to_components_in_expr(expr, lilypond_comments):
    r'''.. versionadded:: 2.3

    Attach `lilypond_comments` to components in `expr`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> lilypond_comment = marktools.LilyPondComment('foo', 'right')
        abjad> marktools.attach_lilypond_comments_to_components_in_expr(staff.leaves, [lilypond_comment])

    ::

        abjad> f(staff)
        \new Staff {
            c'8 % foo
            d'8 % foo
            e'8 % foo
            f'8 % foo
        }

    Return none.
    '''
    from abjad.tools import componenttools

    for component in componenttools.iterate_components_forward_in_expr(expr):
        for lilypond_comment in lilypond_comments:
            LilyPondComment(lilypond_comment)(component)
