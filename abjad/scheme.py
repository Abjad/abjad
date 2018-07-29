"""
Tools for modeling Scheme datastructures used in LilyPond.
"""

import functools
import typing
from abjad import enums
from abjad import typings
from abjad.mathtools.NonreducedFraction import NonreducedFraction
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.utilities.String import String



class Scheme(AbjadValueObject):
    r"""
    Abjad model of Scheme code.

    ..  container:: example

        A Scheme boolean value:

        >>> scheme = abjad.Scheme(True)
        >>> print(format(scheme))
        ##t

    ..  container:: example

        A nested Scheme expession:

        >>> scheme = abjad.Scheme([
        ...     ('left', (1, 2, False)),
        ...     ('right', (1, 2, 3.3)),
        ...     ])
        >>> print(format(scheme))
        #((left (1 2 #f)) (right (1 2 3.3)))

    ..  container:: example

        A list:

        >>> scheme_1 = abjad.Scheme([1, 2, 3])
        >>> scheme_2 = abjad.Scheme((1, 2, 3))
        >>> format(scheme_1) == format(scheme_2)
        True

        Scheme wraps nested variable-length arguments in a tuple.

    ..  container:: example

        A quoted Scheme expression:

        >>> scheme = abjad.Scheme((1, 2, 3), quoting="'#")
        >>> print(format(scheme))
        #'#(1 2 3)

        Use the ``quoting`` keyword to prepend Scheme's various quote, unquote,
        unquote-splicing characters to formatted output.

    ..  container:: example

        A Scheme expression with forced quotes:

        >>> scheme = abjad.Scheme('nospaces', force_quotes=True)
        >>> print(format(scheme))
        #"nospaces"

        Use this in certain \override situations when LilyPond's Scheme
        interpreter treats unquoted strings as symbols instead of strings.
        The string must contain no whitespace for this to work.

    ..  container:: example

        A Scheme expression of LilyPond functions:

        >>> function_1 = 'tuplet-number::append-note-wrapper'
        >>> function_2 = 'tuplet-number::calc-denominator-text'
        >>> string = abjad.Scheme('4', force_quotes=True)
        >>> scheme = abjad.Scheme([function_1, function_2, string])
        >>> abjad.f(scheme)
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

        >>> print(format(scheme))
        #(tuplet-number::append-note-wrapper tuplet-number::calc-denominator-text "4")

    ..  container:: example

        A Scheme lambda expression of LilyPond function that takes a markup
        with a quoted string argument. Setting verbatim to true causes the
        expression to format exactly as-is without modifying quotes or
        whitespace:

        >>> string = '(lambda (grob) (grob-interpret-markup grob'
        >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        >>> scheme = abjad.Scheme(string, verbatim=True)
        >>> abjad.f(scheme)
        abjad.Scheme(
            '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))',
            verbatim=True,
            )

        >>> print(format(scheme))
        #(lambda (grob) (grob-interpret-markup grob #{ \markup \musicglyph #"noteheads.s0harmonic" #}))

    ..  container:: example

        More examples:

        >>> abjad.Scheme(True)
        Scheme(True)

        >>> abjad.Scheme(False)
        Scheme(False)

        >>> abjad.Scheme(None)
        Scheme(None)

        >>> abjad.Scheme('hello')
        Scheme('hello')

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

        Scheme takes an optional ``quoting`` keyword, for prepending
        quote/unquote ticks:

        >>> str(abjad.Scheme(['fus', 'ro', 'dah'], quoting = "',"))
        "',(fus ro dah)"

    ..  container:: example

        __str__ of abjad.Scheme returns the abjad.Scheme formatted value
        without the hash mark, while format(Scheme) returns the formatted value
        with the hash mark, allowing for nested abjad.Scheme expressions:

        >>> scheme = abjad.Scheme(['fus', 'ro', 'dah'], quoting = "'")
        >>> str(scheme)
        "'(fus ro dah)"

        >>> format(scheme)
        "#'(fus ro dah)"

    ..  container:: example

        Scheme attempts to format Python values into abjad.Scheme equivalents:

        >>> format(abjad.Scheme(True))
        '##t'

        >>> format(abjad.Scheme(False))
        '##f'

        >>> format(abjad.Scheme(None))
        '##f'

        >>> format(abjad.Scheme('hello world'))
        '#"hello world"'

        >>> format(abjad.Scheme([1, 2, 3]))
        '#(1 2 3)'

        >>> format(abjad.Scheme([
        ...     abjad.SchemePair(('padding', 1)),
        ...     abjad.SchemePair(('attach-dir', -1)),
        ...     ],
        ...     quoting="'",
        ...     ))
        "#'((padding . 1) (attach-dir . -1))"

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_force_quotes',
        '_quoting',
        '_value',
        '_verbatim',
        )

    _publish_storage_format = True

    lilypond_color_constants = (
        'black',
        'blue',
        'center',
        'cyan',
        'darkblue',
        'darkcyan',
        'darkgreen',
        'darkmagenta',
        'darkred',
        'darkyellow',
        'down',
        'green',
        'grey',
        'left',
        'magenta',
        'red',
        'right',
        'up',
        'white',
        'yellow',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.Any = None,
        force_quotes: bool = None,
        quoting: str = None,
        verbatim: bool = None,
        ) -> None:
        self._value = value
        if force_quotes is not None:
            force_quotes = bool(force_quotes)
        self._force_quotes = force_quotes
        if quoting is not None and not set(r"',@`#").issuperset(set(quoting)):
            message = rf"quoting must be ' or , or @ or ` or #: {quoting!r}."
            raise ValueError(message)
        self._quoting = quoting
        if verbatim is not None:
            verbatim = bool(verbatim)
        self._verbatim = verbatim

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats scheme.

        ..  container:: example

            Scheme LilyPond format:

            >>> scheme = abjad.Scheme('foo')
            >>> format(scheme)
            '#foo'

        ..  container:: example

            Scheme storage format:

            >>> abjad.f(scheme)
            abjad.Scheme(
                'foo'
                )

        """
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        assert format_specification == 'storage'
        return StorageFormatManager(self).get_storage_format()

    def __str__(self) -> str:
        """
        Gets string representation of Scheme object.
        """
        string = self._get_formatted_value()
        if self.quoting is not None:
            string = self.quoting + string
        return string

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            )

    def _get_formatted_value(self):
        return Scheme.format_scheme_value(
            self.value,
            force_quotes=self.force_quotes,
            verbatim=self.verbatim,
            )

    def _get_lilypond_format(self):
        string = self._get_formatted_value()
        if self.quoting is not None:
            string = self.quoting + string
        if string in ('#t', '#f') or not string.startswith('#'):
            string = '#' + string
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def force_quotes(self) -> typing.Optional[bool]:
        """
        Is true when quotes should be forced in output.
        """
        return self._force_quotes

    @property
    def quoting(self) -> typing.Optional[str]:
        """
        Gets Scheme quoting string.
        """
        return self._quoting

    @property
    def value(self) -> typing.Any:
        """
        Gets value.
        """
        return self._value

    @property
    def verbatim(self) -> typing.Optional[bool]:
        """
        Is true when formatting should format value absolutely verbatim.
        Whitespace, quotes, and all other parts of value are left intact.
        """
        return self._verbatim

    ### PUBLIC METHODS ###

    @staticmethod
    def format_embedded_scheme_value(
        value: typing.Any,
        force_quotes: bool = False,
        ) -> str:
        """
        Formats embedded Scheme ``value``.
        """
        if isinstance(value, (enums.HorizontalAlignment, enums.VerticalAlignment)):
            return '#' + repr(value).lower()
        result = Scheme.format_scheme_value(value, force_quotes=force_quotes)
        if isinstance(value, bool):
            result = '#' + result
        elif isinstance(value, str) and value.startswith('#'):
            pass
        elif isinstance(value, str) and not force_quotes:
            result = '#' + result
        elif isinstance(value, Scheme):
            result = '#' + result
        return result

    @staticmethod
    def format_scheme_value(
        value: typing.Any,
        force_quotes: bool = False,
        verbatim: bool = False,
        ) -> str:
        r"""
        Formats ``value`` as Scheme would.

        ..  container:: example

            Some basic values:

            >>> abjad.Scheme.format_scheme_value(1)
            '1'

            >>> abjad.Scheme.format_scheme_value('foo')
            'foo'

            >>> abjad.Scheme.format_scheme_value('bar baz')
            '"bar baz"'

            >>> abjad.Scheme.format_scheme_value([1.5, True, False])
            '(1.5 #t #f)'

        ..  container:: example

            Strings without whitespace can be forcibly quoted via the
            ``force_quotes`` keyword:

            >>> abjad.Scheme.format_scheme_value(
            ...     'foo',
            ...     force_quotes=True,
            ...     )
            '"foo"'

        ..  container:: example

            Set verbatim to true to format value exactly (with only hash
            preprended):

            >>> string = '(lambda (grob) (grob-interpret-markup grob'
            >>> string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
            >>> abjad.Scheme.format_scheme_value(string, verbatim=True)
            '(lambda (grob) (grob-interpret-markup grob #{ \\markup \\musicglyph #"noteheads.s0harmonic" #}))'

        ..  container:: example

            Hash symbol at the beginning of a string does not result in quoted
            output:

            >>> string = '#1-finger'
            >>> abjad.Scheme.format_scheme_value(string)
            '#1-finger'

        """
        if isinstance(value, str) and verbatim:
            return value
        elif isinstance(value, str) and not verbatim:
            value = value.replace('"', r'\"')
            if value.startswith('#'):
                pass
            elif force_quotes or ' ' in value or '#' in value:
                return f'"{value}"'
            return value
        elif value is True:
            return '#t'
        elif value is False:
            return '#f'
        elif isinstance(value, (list, tuple)):
            string = ' '.join(Scheme.format_scheme_value(_) for _ in value)
            return f'({string})'
        elif isinstance(value, Scheme):
            return str(value)
        elif value is None:
            return '#f'
        return str(value)


class SchemeAssociativeList(Scheme):
    """
    Abjad model of Scheme associative list.

    ..  container:: example

        >>> scheme_alist = abjad.SchemeAssociativeList([
        ...     ('space', 2),
        ...     ('padding', 0.5),
        ...     ])
        >>> abjad.f(scheme_alist)
        abjad.SchemeAssociativeList(
            [
                abjad.SchemePair(('space', 2)),
                abjad.SchemePair(('padding', 0.5)),
                ]
            )

        >>> print(format(scheme_alist))
        #'((space . 2) (padding . 0.5))

    Scheme associative lists are immutable.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.List = None,
        ) -> None:
        value = value or []
        pairs = []
        for item in value:
            if isinstance(item, tuple):
                pair = SchemePair(item)
            elif isinstance(item, SchemePair):
                pair = item
            else:
                message = f'must be Python pair or Scheme pair: {item!r}.'
                raise TypeError(message)
            pairs.append(pair)
        Scheme.__init__(self, value=pairs, quoting="'")


class SchemeColor(Scheme):
    r"""
    Abjad model of Scheme color.

    ..  container:: example

        >>> abjad.SchemeColor('ForestGreen')
        SchemeColor('ForestGreen')


    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> scheme_color = abjad.SchemeColor('ForestGreen')
        >>> abjad.override(note).note_head.color = scheme_color
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            \once \override NoteHead.color = #(x11-color 'ForestGreen)
            c'4

    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _get_formatted_value(self):
        string = "(x11-color '{})"
        string = string.format(self._value)
        return string


@functools.total_ordering
class SchemeMoment(Scheme):
    """
    Abjad model of Scheme moment.

    ..  container:: example

        Initializes with two integers:

        >>> abjad.SchemeMoment((2, 68))
        SchemeMoment((2, 68))

    Scheme moments are immutable.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        duration: typing.Union[typing.Tuple[int, int]] = (0, 1),
        ) -> None:
        pair = NonreducedFraction(duration).pair
        Scheme.__init__(self, pair)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a scheme moment with the same value as
        that of this scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((2, 68)) == abjad.SchemeMoment((2, 68))
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.SchemeMoment((2, 54)) == abjad.SchemeMoment((2, 68))
            False

        """
        return super().__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes scheme moment.

        Redefined in tandem with ``__eq__``.
        """
        return super().__hash__()

    def __lt__(self, argument) -> bool:
        """
        Is true when ``argument`` is a scheme moment with value greater than
        that of this scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((1, 68)) < abjad.SchemeMoment((1, 32))
            True

        ..  container:: example

            Otherwise false:

            >>> abjad.SchemeMoment((1, 68)) < abjad.SchemeMoment((1, 78))
            False

        """
        if isinstance(argument, type(self)):
            if self.duration < argument.duration:
                return True
        return False

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    def _get_formatted_value(self):
        pair = self.duration.pair
        string = f'(ly:make-moment {pair[0]} {pair[1]})'
        return string

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> NonreducedFraction:
        """
        Gets duration of Scheme moment.

        ..  container:: example

            >>> abjad.SchemeMoment((2, 68)).duration
            NonreducedFraction(2, 68)

        """
        return NonreducedFraction(self.value)


class SchemePair(Scheme):
    r"""
    Abjad model of Scheme pair.

    ..  container:: example

        Initializes from two values:

        >>> abjad.SchemePair(('spacing', 4))
        SchemePair(('spacing', 4))

    ..  container:: example

        REGRESSION:

        Right-hand side string forces quotes:

        >>> scheme_pair = abjad.SchemePair(('font-name', 'Times'))
        >>> format(scheme_pair)
        '#\'(font-name . "Times")'

        Right-hand side nonstring does not force quotes:

        >>> scheme_pair = abjad.SchemePair(('spacing', 4))
        >>> format(scheme_pair)
        "#'(spacing . 4)"

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_value',
        )

    ### INITIALIZER ##

    def __init__(
        self,
        value = (None, None),
        ) -> None:
        assert isinstance(value, tuple), repr(value)
        assert len(value) == 2, repr(value)
        Scheme.__init__(self, value=value)

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats Scheme pair.

        ..  container:: example

            >>> scheme_pair = abjad.SchemePair((-1, 1))

            >>> format(scheme_pair)
            "#'(-1 . 1)"

            >>> abjad.f(scheme_pair)
            abjad.SchemePair((-1, 1))

        """
        return super().__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.value]
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _get_formatted_value(self):
        assert len(self._value) == 2
        lhs = Scheme.format_scheme_value(self._value[0])
        # need to force quotes around pairs like
        # \override #'(font-name . "Times")
        rhs = Scheme.format_scheme_value(
            self._value[-1],
            force_quotes=True,
            )
        return f'({lhs} . {rhs})'

    def _get_lilypond_format(self):
        string = self._get_formatted_value()
        return f"#'{string}"

    ### PUBLIC PROPERTIES ###

    @property
    def left(self) -> typing.Any:
        """
        Gets left value.
        """
        pair = self.value
        assert isinstance(pair, tuple)
        return pair[0]

    @property
    def right(self) -> typing.Any:
        """
        Gets right value.
        """
        pair = self.value
        assert isinstance(pair, tuple)
        return pair[-1]


class SchemeSymbol(Scheme):
    """
    Abjad model of Scheme symbol.

    ..  container:: example

        >>> scheme = abjad.SchemeSymbol('cross')
        >>> scheme
        SchemeSymbol('cross')

        >>> print(format(scheme))
        #'cross

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        symbol: str = 'cross',
        ) -> None:
        symbol = str(symbol)
        Scheme.__init__(self, value=symbol, quoting="'")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = [self.symbol]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

    @property
    def symbol(self) -> str:
        """
        Gets symbol string.
        """
        assert isinstance(self.value, str)
        return self.value


class SchemeVector(Scheme):
    """
    Abjad model of Scheme vector.

    ..  container:: example

        Scheme vector of boolean values:

        >>> scheme = abjad.SchemeVector([True, True, False])
        >>> scheme
        SchemeVector(True, True, False)
        >>> print(format(scheme))
        #'(#t #t #f)

    ..  container:: example

        Scheme vector of symbols:

        >>> scheme = abjad.SchemeVector(['foo', 'bar', 'blah'])
        >>> scheme
        SchemeVector('foo', 'bar', 'blah')
        >>> print(format(scheme))
        #'(foo bar blah)

    Scheme vectors and Scheme vector constants differ in only their LilyPond
    input format.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.List = [],
        ) -> None:
        Scheme.__init__(self, value, quoting="'")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = self._value
        if String.is_string(self._value):
            values = [self._value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )


class SchemeVectorConstant(Scheme):
    """
    Abjad model of Scheme vector constant.

    ..  container:: example

        Scheme vector constant of boolean values:

        >>> scheme = abjad.SchemeVectorConstant([True, True, False])
        >>> scheme
        SchemeVectorConstant(True, True, False)
        >>> print(format(scheme))
        #'#(#t #t #f)

    Scheme vectors and Scheme vector constants differ in only their LilyPond
    input format.
    """

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        value: typing.List = [],
        ) -> None:
        Scheme.__init__(self, value, quoting="'#")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = self._value
        if String.is_string(self._value):
            values = [self._value]
        return FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )


class SpacingVector(SchemeVector):
    r"""
    Abjad model of Scheme spacing vector.

    ..  container:: example

        >>> vector = abjad.SpacingVector(0, 0, 12, 0)

        >>> abjad.f(vector)
        abjad.SpacingVector(
            abjad.SchemePair(('basic-distance', 0)),
            abjad.SchemePair(('minimum-distance', 0)),
            abjad.SchemePair(('padding', 12)),
            abjad.SchemePair(('stretchability', 0))
            )

        Use to set paper block spacing attributes:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_file = abjad.LilyPondFile.new(staff)
        >>> vector = abjad.SpacingVector(0, 0, 12, 0)
        >>> lilypond_file.paper_block.system_system_spacing = vector

        ..  docs::

            >>> abjad.f(lilypond_file.paper_block)
            \paper {
                system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        basic_distance: typings.Number = 0,
        minimum_distance: typings.Number = 0,
        padding: typings.Number = 12,
        stretchability: typings.Number = 0,
        ) -> None:
        pairs = [
            SchemePair(('basic-distance', basic_distance)),
            SchemePair(('minimum-distance', minimum_distance)),
            SchemePair(('padding', padding)),
            SchemePair(('stretchability', stretchability)),
            ]
        return SchemeVector.__init__(self, pairs)
