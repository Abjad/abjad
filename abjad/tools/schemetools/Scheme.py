# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Scheme(AbjadObject):
    r'''Abjad model of Scheme code.

    ::

        >>> scheme = schemetools.Scheme(True)
        >>> format(scheme)
        '##t'

    Scheme can represent nested structures:

    ::

        >>> scheme = schemetools.Scheme(
        ...     ('left', (1, 2, False)), ('right', (1, 2, 3.3)))
        >>> format(scheme)
        '#((left (1 2 #f)) (right (1 2 3.3)))'

    Scheme wraps variable-length arguments into a tuple:

    ::

        >>> scheme_1 = schemetools.Scheme(1, 2, 3)
        >>> scheme_2 = schemetools.Scheme((1, 2, 3))
        >>> format(scheme_1) == format(scheme_2)
        True

    Scheme also takes an optional `quoting` keyword,
    by which Scheme's various quote, unquote, unquote-splicing characters
    can be prepended to the formatted result:

    ::

        >>> scheme = schemetools.Scheme((1, 2, 3), quoting="'#")
        >>> format(scheme)
        "#'#(1 2 3)"

    Scheme can also force quotes around strings which contain no whitespace:

    ::

        >>> scheme = schemetools.Scheme('nospaces', force_quotes=True)
        >>> print format(scheme)
        #"nospaces"

    The above is useful in certain \override situations,
    as LilyPond's Scheme interpreter
    will treat unquoted strings as symbols rather than strings.

    Scheme is immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_quotes',
        '_quoting',
        '_value',
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
        assert isinstance(quoting, (str, type(None)))
        if quoting is not None:
            assert all(x in ("'", ',', '@', '`', '#') for x in quoting)
        self._force_quotes = force_quotes
        self._quoting = quoting
        self._value = args

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a scheme object with a value equal to that 
        of this scheme object. Otherwise false.

        Returns boolean.
        '''
        if type(self) == type(expr):
            if self._value == expr._value:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats scheme.

        Set `format_specification` to `''`', `'lilypond'` or ``'storage'``.
        Interprets `''` equal to `'lilypond'`.

        ::

            >>> scheme = schemetools.Scheme('foo')
            >>> format(scheme)
            '#foo'

        ::

            >>> print format(scheme, 'storage')
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
            self._value, force_quotes=self.force_quotes)

    @property
    def _lilypond_format(self):
        if self._quoting is not None:
            return '#' + self._quoting + self._formatted_value
        return '#%s' % self._formatted_value

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        if isinstance(self._value, basestring):
            positional_argument_values = (self._value,)
        else:
            positional_argument_values = self._value
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def format_embedded_scheme_value(value, force_quotes=False):
        r'''Formats `value` as an embedded Scheme value.
        '''
        from abjad.tools import schemetools
        result = Scheme.format_scheme_value(value, force_quotes=force_quotes)
        if isinstance(value, bool):
            result = '#{}'.format(result)
        elif isinstance(value, str) and not force_quotes:
            result = '#{}'.format(result)
        elif isinstance(value, schemetools.Scheme):
            result = '#{}'.format(result)
        return result

    @staticmethod
    def format_scheme_value(value, force_quotes=False):
        r'''Formats `value` as Scheme would.

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

        Strings without whitespace can be forcibly quoted via the
        `force_quotes` keyword:

        ::

            >>> schemetools.Scheme.format_scheme_value(
            ...     'foo', force_quotes=True)
            '"foo"'

        Returns string.
        '''
        from abjad.tools import schemetools
        if isinstance(value, str):
            value = value.replace('"', r'\"')
            if -1 == value.find(' ') and not force_quotes:
                return value
            return '"{}"'.format(value)
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

        Returns boolean.
        '''
        return self._force_quotes
