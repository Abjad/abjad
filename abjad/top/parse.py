import typing


_lilypond_parsers_by_language = {}  # type: typing.Dict[str, LilyPondParser]


def parse(string, language='english'):
    r"""
    Parses LilyPond ``string``.

    ..  container:: example

        Parses LilyPond string with English note names:

        >>> container = abjad.parse("{c'4 d'4 e'4 f'4}")
        >>> abjad.show(container) # doctest: +SKIP

    ..  container:: example

        Parses LilyPond string with Dutch note names:

        >>> container = abjad.parse(
        ...     "{c'8 des' e' fis'}",
        ...     language='nederlands',
        ...     )
        >>> abjad.show(container) # doctest: +SKIP

    Returns Abjad component.
    """
    from abjad import rhythmtree
    from abjad import parser as abjad_parser
    if string.startswith('abj:'):
        return abjad_parser.parse_reduced_ly_syntax(string[4:])
    elif string.startswith('rtm:'):
        return rhythmtree.parse_rtm_syntax(string[4:])
    if language not in _lilypond_parsers_by_language:
        parser = abjad_parser.LilyPondParser(default_language=language)
        _lilypond_parsers_by_language[language] = parser
    return _lilypond_parsers_by_language[language](string)
