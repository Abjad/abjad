# -*- encoding: utf-8 -*-
from abjad.tools import schemetools


def smaller(markup):
    r'''LilyPond ``\smaller`` markup command.

    ..  container:: example

        ::

            >>> markup = Markup('Allegro assai')
            >>> markup = markuptools.smaller(markup)

        ::

            >>> print(format(markup))
            \markup {
                \smaller
                    "Allegro assai"
                }

        ::

            >>> show(markup) # doctest: +SKIP

    Returns markup.
    '''
    from abjad.tools import markuptools
    prototype = (str, markuptools.Markup, markuptools.MarkupCommand)
    assert isinstance(markup, prototype), repr(markup)

    if isinstance(markup, markuptools.Markup):
        if len(markup.contents) == 1:
            contents = markup.contents[0]
        else:
            contents = list(markup.contents)
    elif isinstance(markup, (str, markuptools.MarkupCommand)):
        contents = markup
    else:
        raise TypeError(markup)

    command = markuptools.MarkupCommand(
        'smaller',
        contents,
        )
    markup = markuptools.Markup(command)

    return markup