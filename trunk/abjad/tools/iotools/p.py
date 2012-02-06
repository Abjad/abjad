def p(*args):
    r'''.. versionadded:: 2.7

    Parse `args` as LilyPond string::

        abjad> p("{c'4 d'4 e'4 f'4}")
        {c'4, d'4, e'4, f'4}

    ::

        abjad> container = _
        abjad> f(container)
        {
            c'4
            d'4
            e'4
            f'4
        }

    A pitch-name language may also be specified.

    ::

        abjad> p("{c'8 des' e' fis'}", 'nederlands')
        {c'8, df'8, e'8, fs'8}

    Return Abjad expression.
    '''
    from abjad.tools.lilypondparsertools import LilyPondParser

    if 1 < len(args):
        return LilyPondParser(default_language=args[1])(args[0])
    return LilyPondParser()(args[0])
