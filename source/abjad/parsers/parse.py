from .parser import LilyPondParser
from .reduced import parse_reduced_ly_syntax

_lilypond_parsers_by_language: dict = {}


def parse(string: str, language: str = "english", *, tag=None):
    r"""
    Parses LilyPond ``string``.

    ..  container:: example

        Parses LilyPond string with English note names:

        >>> container = abjad.parse("{c'4 d'4 e'4 f'4}")
        >>> abjad.show(container) # doctest: +SKIP

        Parses LilyPond string with Dutch note names:

        >>> container = abjad.parse("{c'8 des' e' fis'}", language='nederlands')
        >>> abjad.show(container) # doctest: +SKIP

        Tags output:

        >>> container = abjad.parse("{c'4 d'4 e'4 f'4}", tag=abjad.Tag("FOO"))
        >>> string = abjad.lilypond(container, tags=True)
        >>> print(string)
          %! FOO
        {
              %! FOO
            c'4
              %! FOO
            d'4
              %! FOO
            e'4
              %! FOO
            f'4
          %! FOO
        }

    Returns Abjad component.
    """
    if string.startswith("abj:"):
        return parse_reduced_ly_syntax(string[4:])
    if language not in _lilypond_parsers_by_language:
        parser = LilyPondParser(default_language=language)
        _lilypond_parsers_by_language[language] = parser
    parser = _lilypond_parsers_by_language[language]
    parser.tag = tag
    if hasattr(parser, "_guile"):
        parser._guile.tag = tag
    if hasattr(parser, "_lexdef"):
        parser._lexdef.tag = tag
    if hasattr(parser, "_syndef"):
        parser._syndef.tag = tag
    result = parser(string)
    return result
