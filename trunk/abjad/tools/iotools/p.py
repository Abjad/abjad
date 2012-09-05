def p(*args):
    r'''.. versionadded:: 2.7

    Parse `args` as LilyPond string::

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

        >>> p("{c'8 des' e' fis'}", 'nederlands')
        {c'8, df'8, e'8, fs'8}

    Return Abjad expression.
    '''
    # TODO: lilypondparsertools should NOT depend on iotools.
    #       The direction of dependency should be the other way around.
    from abjad.tools import lilypondparsertools

    if 1 < len(args):
        return lilypondparsertools.LilyPondParser(default_language=args[1])(args[0])
    return lilypondparsertools.LilyPondParser()(args[0])
