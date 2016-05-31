# -*- coding: utf-8 -*-


_lilypond_parsers_by_language = {}


def parse(arg, language='english'):
    r'''Parses `arg` as LilyPond string.

    ::

        >>> parse("{c'4 d'4 e'4 f'4}")
        Container("c'4 d'4 e'4 f'4")

    ::

        >>> container = _

    ::

        >>> print(format(container))
        {
            c'4
            d'4
            e'4
            f'4
        }

    A pitch-name language may also be specified.

    ::

        >>> parse("{c'8 des' e' fis'}", language='nederlands')
        Container("c'8 df'8 e'8 fs'8")

    Returns Abjad expression.
    '''
    from abjad.tools import rhythmtreetools
    from abjad.tools import lilypondparsertools
    if arg.startswith('abj:'):
        return lilypondparsertools.parse_reduced_ly_syntax(arg[4:])
    elif arg.startswith('rtm:'):
        return rhythmtreetools.parse_rtm_syntax(arg[4:])
    if language not in _lilypond_parsers_by_language:
        parser = lilypondparsertools.LilyPondParser(default_language=language)
        _lilypond_parsers_by_language[language] = parser
    return _lilypond_parsers_by_language[language](arg)
