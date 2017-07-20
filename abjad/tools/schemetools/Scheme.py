# -*- coding: utf-8 -*-
import collections
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Scheme(AbjadValueObject):
    r'''Abjad model of Scheme code.

    ::

        >>> import abjad

    ..  container:: example

        A Scheme boolean value:

        ::

            >>> scheme = abjad.Scheme(True)
            >>> print(format(scheme))
            ##t

    ..  container:: example

        A nested Scheme expession:

        ::

            >>> scheme = abjad.Scheme([
            ...     ('left', (1, 2, False)),
            ...     ('right', (1, 2, 3.3)),
            ...     ])
            >>> print(format(scheme))
            #((left (1 2 #f)) (right (1 2 3.3)))

    ..  container:: example

        A list:

        ::

            >>> scheme_1 = abjad.Scheme([1, 2, 3])
            >>> scheme_2 = abjad.Scheme((1, 2, 3))
            >>> format(scheme_1) == format(scheme_2)
            True

        Scheme wraps nested variable-length arguments in a tuple.

    ..  container:: example

        A quoted Scheme expression:

        ::

            >>> scheme = abjad.Scheme((1, 2, 3), quoting="'#")
            >>> print(format(scheme))
            #'#(1 2 3)

        Use the `quoting` keyword to prepend Scheme's various quote, unquote,
        unquote-splicing characters to formatted output.

    ..  container:: example

        A Scheme expression with forced quotes:

        ::

            >>> scheme = abjad.Scheme('nospaces', force_quotes=True)
            >>> print(format(scheme))
            #"nospaces"

        Use this in certain \override situations when LilyPond's Scheme
        interpreter treats unquoted strings as symbols instead of strings.
        The string must contain no whitespace for this to work.

    ..  container:: example

        A Scheme expression of LilyPond functions:

        ::

            >>> function_1 = 'tuplet-number::append-note-wrapper'
            >>> function_2 = 'tuplet-number::calc-denominator-text'
            >>> string = abjad.Scheme('4', force_quotes=True)
            >>> scheme = abjad.Scheme([function_1, function_2, string])
            >>> f(scheme)
            abjad.Scheme(
                [
                    'tuplet-number::append-note-wrapper',
                    'tuplet-number::calc-denominator-text',
                    abjad.Scheme(
                        '4',
                        force_quotes=True,
                        ),
                    ]
                )

        ::

            >>> print(format(scheme))
            #(tuplet-number::append-note-wrapper tuplet-number::calc-denominator-text "4")

    ..  container:: example

        A Scheme lambda expression of LilyPond function that takes a markup
        with a quoted string argument. Setting verbatim to true causes the
        expression to format exactly as-is without modifying quotes or
        whitespace:

        ::

            >>> string = '(lambda (grob) (grob-interpret-markup grob'
            >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
            >>> scheme = abjad.Scheme(string, verbatim=True)
            >>> f(scheme)
            abjad.Scheme(
                '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))',
                verbatim=True,
                )

        ::

            >>> print(format(scheme))
            #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))

    ..  container:: example

        More examples:

        ::

            >>> abjad.Scheme(True)
            Scheme(True)

        ::

            >>> abjad.Scheme(False)
            Scheme(False)

        ::

            >>> abjad.Scheme(None)
            Scheme(None)

        ::

            >>> abjad.Scheme('hello')
            Scheme('hello')

        ::

            >>> abjad.Scheme('hello world')
            Scheme('hello world')

            >>> abjad.Scheme([abjad.Scheme('foo'), abjad.Scheme(3.14159)])
            Scheme([Scheme('foo'), Scheme(3.14159)])

            >>> abjad.Scheme([
            ...     abjad.SchemePair(('padding', 1)),
            ...     abjad.SchemePair(('attach-dir', -1)),
            ...     ])
            Scheme([SchemePair(('padding', 1)), SchemePair(('attach-dir', -1))])

    ..  container:: example

        Scheme takes an optional `quoting` keyword, for prepending
        quote/unquote ticks:

        >>> str(abjad.Scheme(['fus', 'ro', 'dah'], quoting = "',"))
        "',(fus ro dah)"

    ..  container:: example

        __str__ of abjad.Scheme returns the abjad.Scheme formatted value
        without the hash mark, while format(Scheme) returns the formatted value
        with the hash mark, allowing for nested abjad.Scheme expressions:

        ::

            >>> scheme = abjad.Scheme(['fus', 'ro', 'dah'], quoting = "'")
            >>> str(scheme)
            "'(fus ro dah)"

        ::

            >>> format(scheme)
            "#'(fus ro dah)"

    ..  container:: example

        Scheme attempts to format Python values into abjad.Scheme equivalents:

        ::

            >>> format(abjad.Scheme(True))
            '##t'

        ::

            >>> format(abjad.Scheme(False))
            '##f'

        ::

            >>> format(abjad.Scheme(None))
            '##f'

        ::

            >>> format(abjad.Scheme('hello world'))
            '#"hello world"'

        ::


            >>> format(abjad.Scheme([1, 2, 3]))
            '#(1 2 3)'

        ::

            >>> format(abjad.Scheme([
            ...     abjad.SchemePair(('padding', 1)),
            ...     abjad.SchemePair(('attach-dir', -1)),
            ...     ],
            ...     quoting="'",
            ...     ))
            "#'((padding . 1) (attach-dir . -1))"

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_quotes',
        '_quoting',
        '_value',
        '_verbatim',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        value=None,
        force_quotes=None,
        quoting=None,
        verbatim=None,
        ):
        if quoting is not None:
            if (not isinstance(quoting, str) or
                not all(character in r"',@`#" for character in quoting)):
                message = r"quoting must be ' or , or @ or ` or #: {!r}."
                message = message.format(quoting)
                raise ValueError(message)
        if not isinstance(force_quotes, (bool, type(None))):
            message = 'force quotes must be true, false or none: {!r}.'
            message = message.format(force_quotes)
            raise TypeError(force_quotes)
        if not isinstance(verbatim, (bool, type(None))):
            message = 'force quotes must be true, false or none: {!r}.'
            message = message.format(verbatim)
            raise TypeError(verbatim)
        self._value = value
        self._quoting = quoting
        self._force_quotes = force_quotes
        self._verbatim = verbatim

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats scheme.

        Set `format_specification` to `''`', `'lilypond'` or ``'storage'``.
        Interprets `''` equal to `'lilypond'`.

        ..  container:: example

            Scheme LilyPond format:

            ::

                >>> scheme = abjad.Scheme('foo')
                >>> format(scheme)
                '#foo'

        ..  container:: example

            Scheme storage format:

            ::

                >>> f(scheme)
                abjad.Scheme(
                    'foo'
                    )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __str__(self):
        r'''String representation of scheme object.

        Returns string.
        '''
        if self._quoting is not None:
            return self._quoting + self._formatted_value
        return self._formatted_value

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        return Scheme.format_scheme_value(
            self._value,
            force_quotes=self.force_quotes,
            verbatim=self.verbatim,
            )

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    def _get_lilypond_format(self):
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#' + self._formatted_value

    ### PUBLIC PROPERTIES ###

    @property
    def force_quotes(self):
        r'''Is true when quotes should be forced in output. Otherwise false.

        Returns true or false.
        '''
        return self._force_quotes

    @property
    def quoting(self):
        r'''Gets Scheme quoting string.

        Returns string.
        '''
        return self._quoting

    @property
    def value(self):
        r'''Gets value.
        '''
        return self._value

    @property
    def verbatim(self):
        r'''Is true when formatting should format value absolutely verbatim.
        Whitespace, quotes, and all other parts of value are left intact.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._verbatim

    ### PUBLIC METHODS ###

    @staticmethod
    def format_embedded_scheme_value(value, force_quotes=False):
        r'''Formats `value` as an embedded Scheme value.
        '''
        from abjad.tools import datastructuretools
        if isinstance(value, datastructuretools.OrdinalConstant):
            result = '#' + repr(value).lower()
        else:
            result = Scheme.format_scheme_value(
                value, force_quotes=force_quotes)
            if (
                (isinstance(value, bool)) or
                (isinstance(value, str) and not force_quotes) or
                (isinstance(value, Scheme))
                ):
                result = '#' + result
        return result

    @staticmethod
    def format_scheme_value(value, force_quotes=False, verbatim=False):
        r'''Formats `value` as Scheme would.

        ..  container:: example

            Some basic values:

            ::

                >>> abjad.Scheme.format_scheme_value(1)
                '1'

            ::

                >>> abjad.Scheme.format_scheme_value('foo')
                'foo'

            ::

                >>> abjad.Scheme.format_scheme_value('bar baz')
                '"bar baz"'

            ::

                >>> abjad.Scheme.format_scheme_value([1.5, True, False])
                '(1.5 #t #f)'

        ..  container:: example

            Strings without whitespace can be forcibly quoted via the
            `force_quotes` keyword:

            ::

                >>> abjad.Scheme.format_scheme_value(
                ...     'foo',
                ...     force_quotes=True,
                ...     )
                '"foo"'

        ..  container:: example

            Set verbatim to true to format value exactly (with only hash
            preprended):

            ::

                >>> string = '(lambda (grob) (grob-interpret-markup grob'
                >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
                >>> abjad.Scheme.format_scheme_value(string, verbatim=True)
                '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))'

        ..  container:: example

            Hash symbols in strings will result in quoted output unless
            `verbatim` is True, in order to prevent LilyPond parsing errors:

            ::

                >>> string = '#1-finger'
                >>> abjad.Scheme.format_scheme_value(string)
                '"#1-finger"'

            ::

                >>> abjad.Scheme.format_scheme_value(string, verbatim=True)
                '#1-finger'

        Returns string.
        '''
        if isinstance(value, str):
            if not verbatim:
                value = value.replace('"', r'\"')
                if force_quotes or ' ' in value or '#' in value:
                    return '"{}"'.format(value)
                return value
            else:
                return value
        elif isinstance(value, bool):
            if value:
                return '#t'
            return '#f'
        elif isinstance(value, (list, tuple)):
            return '({})'.format(
                ' '.join(Scheme.format_scheme_value(x)
                    for x in value))
        elif isinstance(value, Scheme):
            return str(value)
        elif isinstance(value, type(None)):
            return '#f'
        return str(value)
