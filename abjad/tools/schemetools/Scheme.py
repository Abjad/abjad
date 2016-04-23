# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.abctools import AbjadValueObject


class Scheme(AbjadValueObject):
    r'''Abjad model of Scheme code.

    ..  container:: example

        **Example 1.** A Scheme boolean value:

        ::

            >>> scheme = schemetools.Scheme(True)
            >>> print(format(scheme))
            ##t

    ..  container:: example

        **Example 2.** A nested Scheme expession:

        ::

            >>> scheme = schemetools.Scheme(
            ...     ('left', (1, 2, False)),
            ...     ('right', (1, 2, 3.3))
            ...     )
            >>> print(format(scheme))
            #((left (1 2 #f)) (right (1 2 3.3)))

    ..  container:: example

        **Example 3.** A variable-length argument:

        ::

            >>> scheme_1 = schemetools.Scheme(1, 2, 3)
            >>> scheme_2 = schemetools.Scheme((1, 2, 3))
            >>> format(scheme_1) == format(scheme_2)
            True

        Scheme wraps nested variable-length arguments in a tuple.

    ..  container:: example

        **Example 4.** A quoted Scheme expression:

        ::

            >>> scheme = schemetools.Scheme((1, 2, 3), quoting="'#")
            >>> print(format(scheme))
            #'#(1 2 3)

        Use the `quoting` keyword to prepend Scheme's various quote, unquote, 
        unquote-splicing characters to formatted output.

    ..  container:: example

        **Example 5.** A Scheme expression with forced quotes:

        ::

            >>> scheme = schemetools.Scheme('nospaces', force_quotes=True)
            >>> print(format(scheme))
            #"nospaces"

        Use this in certain \override situations when LilyPond's Scheme
        interpreter treats unquoted strings as symbols instead of strings.
        The string must contain no whitespace for this to work.

    ..  container:: example

        **Example 6.** A Scheme expression of LilyPond functions:

        ::

            >>> function_1 = 'tuplet-number::append-note-wrapper'
            >>> function_2 = 'tuplet-number::calc-denominator-text'
            >>> string = schemetools.Scheme('4', force_quotes=True)
            >>> scheme = schemetools.Scheme(
            ...     function_1,
            ...     function_2,
            ...     string,
            ...     )
            >>> scheme
            Scheme('tuplet-number::append-note-wrapper', 'tuplet-number::calc-denominator-text', Scheme('4', force_quotes=True))
            >>> print(format(scheme))
            #(tuplet-number::append-note-wrapper tuplet-number::calc-denominator-text "4")

    ..  container:: example

        **Example 7.** A Scheme lambda expression of LilyPond function that
        takes a markup with a quoted string argument. Setting verbatim to true
        causes the expression to format exactly as-is without modifying quotes
        or whitespace:

        ::

            >>> string = '(lambda (grob) (grob-interpret-markup grob'
            >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
            >>> scheme = schemetools.Scheme(string, verbatim=True)
            >>> scheme
            Scheme('(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))')
            >>> print(format(scheme))
            #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))

    Scheme objects are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_quotes',
        '_quoting',
        '_value',
        '_verbatim',
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        if 1 == len(args):
            if isinstance(args[0], type(self)):
                args = args[0]._value
            else:
                args = args[0]
        quoting = kwargs.get('quoting')
        force_quotes = bool(kwargs.get('force_quotes'))
        verbatim = kwargs.get('verbatim')
        assert isinstance(quoting, (str, type(None)))
        if quoting is not None:
            assert all(x in ("'", ',', '@', '`', '#') for x in quoting)
        self._force_quotes = force_quotes
        self._quoting = quoting
        self._value = args
        self._verbatim = bool(verbatim)

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats scheme.

        Set `format_specification` to `''`', `'lilypond'` or ``'storage'``.
        Interprets `''` equal to `'lilypond'`.

        ..  container:: example

            **Example 1.** Scheme LilyPond format:

            ::

                >>> scheme = schemetools.Scheme('foo')
                >>> format(scheme)
                '#foo'

        ..  container:: example

            **Example 2.** Scheme storage format:

            ::

                >>> print(format(scheme, 'storage'))
                schemetools.Scheme(
                    'foo'
                    )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getnewargs__(self):
        r'''Gets new arguments.

        Returns tuple.
        '''
        return (self._value,)

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
        from abjad.tools import schemetools
        return schemetools.Scheme.format_scheme_value(
            self._value, 
            force_quotes=self.force_quotes,
            verbatim=self.verbatim,
            )

    @property
    def _lilypond_format(self):
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#%s' % self._formatted_value

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        if stringtools.is_string(self._value):
            positional_argument_values = (self._value,)
        else:
            positional_argument_values = self._value
        keyword_argument_names = []
        if self.force_quotes:
            keyword_argument_names.append('force_quotes')
        if self.quoting:
            keyword_argument_names.append('quoting')
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def format_embedded_scheme_value(value, force_quotes=False):
        r'''Formats `value` as an embedded Scheme value.
        '''
        from abjad.tools import datastructuretools
        from abjad.tools import schemetools
        result = Scheme.format_scheme_value(value, force_quotes=force_quotes)
        if isinstance(value, bool):
            result = '#{}'.format(result)
        elif isinstance(value, datastructuretools.OrdinalConstant):
            result = '#{}'.format(repr(value).lower())
        elif isinstance(value, str) and not force_quotes:
            result = '#{}'.format(result)
        elif isinstance(value, schemetools.Scheme):
            result = '#{}'.format(result)
        return result

    @staticmethod
    def format_scheme_value(value, force_quotes=False, verbatim=False):
        r'''Formats `value` as Scheme would.

        ..  container:: example

            **Example 1.** Some basic values:

            ::

                >>> schemetools.Scheme.format_scheme_value(1)
                '1'

            ::

                >>> schemetools.Scheme.format_scheme_value('foo')
                'foo'

            ::

                >>> schemetools.Scheme.format_scheme_value('bar baz')
                '"bar baz"'

            ::

                >>> schemetools.Scheme.format_scheme_value([1.5, True, False])
                '(1.5 #t #f)'

        ..  container:: example

            **Example 2.** Strings without whitespace can be forcibly quoted
            via the `force_quotes` keyword:

            ::

                >>> schemetools.Scheme.format_scheme_value(
                ...     'foo',
                ...     force_quotes=True,
                ...     )
                '"foo"'

        ..  container:: example

            **Example 3.** Set verbatim to true to format value exactly (with
            only hash preprended):

            ::

                >>> string = '(lambda (grob) (grob-interpret-markup grob'
                >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
                >>> schemetools.Scheme.format_scheme_value(string, verbatim=True)
                '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))'

        ..  container:: example

            **Example 4.** Hash symbols in strings will result in quoted output
            unless `verbatim` is True, in order to prevent LilyPond parsing
            errors:

            ::

                >>> string = '#1-finger'
                >>> schemetools.Scheme.format_scheme_value(string)
                '"#1-finger"'

            ::

                >>> schemetools.Scheme.format_scheme_value(string, verbatim=True)
                '#1-finger'

        Returns string.
        '''
        from abjad.tools import schemetools
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
                ' '.join(schemetools.Scheme.format_scheme_value(x)
                    for x in value))
        elif isinstance(value, schemetools.Scheme):
            return str(value)
        elif isinstance(value, type(None)):
            return '#f'
        return str(value)

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

        Return string.
        '''
        return self._quoting

    @property
    def verbatim(self):
        r'''Is true when formatting should format value absolutely verbatim.
        Whitespace, quotes and all other parts of value are left in tact.

        Defaults to false.

        Set to true or false.

        Returns true or false.
        '''
        return self._verbatim
