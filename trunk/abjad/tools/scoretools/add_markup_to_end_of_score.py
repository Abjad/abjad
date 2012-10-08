from abjad.tools import leaftools


def add_markup_to_end_of_score(score, markup, extra_offset=None):
    r'''.. versionadded:: 2.0

    Add `markup` to end of `score`::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> markup = r'\italic \right-column { "Bremen - Boston - LA." "Jul 2010 - May 2011." }'
        >>> markup = markuptools.Markup(markup, Down)
        >>> markup = scoretools.add_markup_to_end_of_score(staff, markup, (4, -2))

    ::

        >>> z(markup)
        markuptools.Markup((
            markuptools.MarkupCommand(
                'italic',
                markuptools.MarkupCommand(
                    'right-column',
                    [
                        'Bremen - Boston - LA.',
                        'Jul 2010 - May 2011.'
                    ]
                    )
                ),
            ),
            direction=Down
            )

    ::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            \once \override TextScript #'extra-offset = #'(4 . -2)
            f'4 _ \markup { 
                \italic
                    \right-column
                        {
                            "Bremen - Boston - LA."
                            "Jul 2010 - May 2011."
                        }
                }
        }

    Return `markup`.
    '''
    from abjad.tools import markuptools

    last_leaf = leaftools.get_nth_leaf_in_expr(score, -1)
    # TODO: copy markup direction from markup input
    markup = markuptools.Markup(markup, Down)(last_leaf)

    if extra_offset is not None:
        last_leaf.override.text_script.extra_offset = extra_offset

    return markup
