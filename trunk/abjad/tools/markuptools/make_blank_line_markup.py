def make_blank_line_markup():
    r'''.. versionadded:: 2.9

    Make blank line markup::

        >>> markup = markuptools.make_blank_line_markup()

    ::

        >>> markup
        Markup((MarkupCommand('fill-line', [' ']),))

    ::

        >>> f(markup)
        \markup { \fill-line { " " } }

    Return markup.
    '''
    from abjad.tools import markuptools
    
    return markuptools.Markup(r'\fill-line { " " }')
