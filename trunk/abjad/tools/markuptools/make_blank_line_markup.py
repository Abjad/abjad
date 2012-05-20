from abjad.tools.markuptools.Markup import Markup


def make_blank_line_markup():
    r'''.. versionadded:: 2.9

    Make blank line markup::

        abjad> markup = markuptools.make_blank_line_markup()

    ::

        abjad> markup
        Markup(('\\fill-line { " " }',))

    ::

        abjad> f(markup)
        \markup { \fill-line { " " } }

    Return markup.
    '''
    
    return Markup(r'\fill-line { " " }')
