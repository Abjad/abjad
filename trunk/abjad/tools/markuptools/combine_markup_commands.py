def combine_markup_commands(*commands):
    r'''Combine MarkupCommand and/or string objects.

    LilyPond's '\combine' markup command can only take two arguments, so in order
    to combine more than two stencils, a cascade of '\combine' commands must be
    employed.  `combine_markup_commands` simplifies this process.

    ::

        >>> from abjad.tools.schemetools import SchemePair

    ::

        >>> markup_a = markuptools.MarkupCommand('draw-circle', 4, 0.4, False)
        >>> markup_b = markuptools.MarkupCommand(
        ...     'filled-box', 
        ...     schemetools.SchemePair(-4, 4), 
        ...     schemetools.SchemePair(-0.5, 0.5), 1)
        >>> markup_c = "some text"

    ::

        >>> markup = markuptools.combine_markup_commands(markup_a, markup_b, markup_c)
        >>> result = markup.lilypond_format

    ::

        >>> print result
        \combine \combine \draw-circle #4 #0.4 ##f 
            \filled-box #'(-4 . 4) #'(-0.5 . 0.5) #1 "some text"

    Returns a markup command instance, or a string if that was the only argument.
    '''
    from abjad.tools import markuptools

    assert len(commands)
    assert all([isinstance(command, (markuptools.MarkupCommand, str)) for command in commands])

    if 1 == len(commands):
        return commands[0]

    combined = markuptools.MarkupCommand('combine', commands[0], commands[1])
    for command in commands[2:]:
        combined = markuptools.MarkupCommand('combine', combined, command)
    return combined
