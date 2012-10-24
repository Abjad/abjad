def p(arg, language='english'):
    r'''.. versionadded:: 2.7

    Parse `arg` as LilyPond string::

        >>> p("{c'4 d'4 e'4 f'4}")
        {c'4, d'4, e'4, f'4}

    ::

        >>> container = _
        >>> f(container)
        {
            c'4
            d'4
            e'4
            f'4
        }

    A pitch-name language may also be specified.

    ::

        >>> p("{c'8 des' e' fis'}", language='nederlands')
        {c'8, df'8, e'8, fs'8}

    Return Abjad expression.
    '''
    # TODO: lilypondparsertools should NOT depend on iotools.
    #       The direction of dependency should be the other way around.
    from abjad.tools import rhythmtreetools
    from abjad.tools import lilypondparsertools

    if arg.startswith('abj:'):
        return lilypondparsertools.parse_reduced_ly_syntax(arg[4:])
    elif arg.startswith('rtm:'):
        return rhythmtreetools.parse_rtm_syntax(arg[4:])
    return lilypondparsertools.LilyPondParser(default_language=language)(arg)
