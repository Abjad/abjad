# -*- encoding: utf-8 -*-
from abjad.tools import schemetools


def with_color(color, markup):
    r'''LilyPond ``\with-color`` markup command.

    ..  container:: example

        ::

            >>> markup = Markup('Allegro assai')
            >>> markup = markuptools.with_color('blue', markup)

        ::

            >>> print(format(markup))
            \markup {
                \with-color
                    #blue
                    {
                        "Allegro assai"
                    }
                }

        ::

            >>> show(markup) # doctest: +SKIP

    Returns markup.
    '''
    from abjad.tools import markuptools
    prototype = (str, markuptools.Markup, markuptools.MarkupCommand)
    assert isinstance(markup, prototype), repr(markup)

    if isinstance(markup, markuptools.Markup):
        contents = list(markup.contents)
    elif isinstance(markup, (str, markuptools.MarkupCommand)):
        contents = markup
    else:
        raise TypeError(markup)

    color = schemetools.Scheme(color)
    command = markuptools.MarkupCommand(
        'with-color',
        color,
        contents,
        )
    markup = markuptools.Markup(command)

    return markup