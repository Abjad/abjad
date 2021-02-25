import typing


def format_scheme_value(
    value: typing.Any, force_quotes: bool = False, verbatim: bool = False
) -> str:
    r"""
    Formats ``value`` in a scheme-like way.

    ..  container:: example

        Some basic values:

        >>> abjad.fsv.format_scheme_value(1)
        '1'

        >>> abjad.fsv.format_scheme_value('foo')
        'foo'

        >>> abjad.fsv.format_scheme_value('bar baz')
        '"bar baz"'

        >>> abjad.fsv.format_scheme_value([1.5, True, False])
        '(1.5 #t #f)'

    ..  container:: example

        Strings without whitespace can be forcibly quoted via the
        ``force_quotes`` keyword:

        >>> abjad.fsv.format_scheme_value(
        ...     'foo',
        ...     force_quotes=True,
        ...     )
        '"foo"'

    ..  container:: example

        Set verbatim to true to format value exactly (with only hash
        preprended):

        >>> string = '(lambda (grob) (grob-interpret-markup grob'
        >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        >>> abjad.fsv.format_scheme_value(string, verbatim=True)
        '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))'

    ..  container:: example

        Hash symbol at the beginning of a string does not result in quoted
        output:

        >>> string = '#1-finger'
        >>> abjad.fsv.format_scheme_value(string)
        '#1-finger'

    """
    if isinstance(value, str) and verbatim:
        return value
    elif isinstance(value, str) and not verbatim:
        value = value.replace('"', r"\"")
        if value.startswith("#"):
            pass
        elif value.startswith("\\"):
            pass
        elif force_quotes or " " in value or "#" in value:
            return f'"{value}"'
        return value
    elif value is True:
        return "#t"
    elif value is False:
        return "#f"
    elif isinstance(value, (list, tuple)):
        string = " ".join(format_scheme_value(_) for _ in value)
        return f"({string})"
    elif value is None:
        return "#f"
    return str(value)
