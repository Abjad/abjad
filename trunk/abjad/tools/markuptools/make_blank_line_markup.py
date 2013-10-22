# -*- encoding: utf-8 -*-


def make_blank_line_markup():
    r'''Make blank line markup:

    ::

        >>> markup = markuptools.make_blank_line_markup()

    ::

        >>> markup
        Markup((MarkupCommand('fill-line', [' ']),))

    ..  doctest::

        >>> f(markup)
        \markup { \fill-line { " " } }

    Returns markup.
    '''
    from abjad.tools import markuptools

    return markuptools.Markup(r'\fill-line { " " }')
