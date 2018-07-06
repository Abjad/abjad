import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.scheme import Scheme
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class LilyPondGrobOverride(AbjadValueObject):
    r"""
    LilyPond grob override.

    ..  container:: example

        >>> override = abjad.LilyPondGrobOverride(
        ...    lilypond_type='Staff',
        ...    grob_name='TextSpanner',
        ...    once=True,
        ...    property_path=(
        ...        'bound-details',
        ...        'left',
        ...        'text',
        ...        ),
        ...    value=abjad.Markup(r'\bold { over pressure }'),
        ...    )

        >>> print(override.override_string)
        \once \override Staff.TextSpanner.bound-details.left.text = \markup {
            \bold
                {
                    over
                    pressure
                }
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_grob_name',
        '_is_revert',
        '_lilypond_type',
        '_once',
        '_property_path',
        '_value',
        )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type: str = None,
        grob_name: str = 'NoteHead',
        once: bool = None,
        is_revert: bool = None,
        property_path: typing.Union[str, typing.Iterable[str]] = 'color',
        value: typing.Any = 'red',
        ) -> None:
        if lilypond_type is not None:
            lilypond_type = str(lilypond_type)
        self._lilypond_type = lilypond_type
        assert grob_name
        self._grob_name = str(grob_name)
        if once is not None:
            once = bool(once)
        self._once = once
        if is_revert is not None:
            is_revert = bool(is_revert)
        self._is_revert = is_revert
        if isinstance(property_path, str):
            property_path_: typing.Tuple[str, ...] = (property_path,)
        else:
            property_path_ = tuple(property_path)
        assert isinstance(property_path_, tuple), repr(property_path_)
        assert all(isinstance(_, str) for _ in property_path_)
        assert all(_ != '' for _ in property_path_)
        self._property_path = property_path_
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond grob override with equivalent
        keyword values.
        """
        return super().__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes LilyPond grob override.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if not self.once:
            revert_format = '\n'.join(self.revert_format_pieces)
            bundle.grob_reverts.append(revert_format)
        if not self.is_revert:
            override_format = '\n'.join(self.override_format_pieces)
            bundle.grob_overrides.append(override_format)
        return bundle

    def _override_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        parts.extend(self.property_path)
        path = '.'.join(parts)
        return path

    def _revert_property_path_string(self):
        parts = []
        if self.lilypond_type is not None:
            parts.append(self.lilypond_type)
        parts.append(self.grob_name)
        parts.append(self.property_path[0])
        path = '.'.join(parts)
        return path

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_type(self) -> typing.Optional[str]:
        r"""
        Gets LilyPond type of context.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...    lilypond_type='Staff',
            ...    grob_name='TextSpanner',
            ...    once=True,
            ...    property_path=(
            ...        'bound-details',
            ...        'left',
            ...        'text',
            ...        ),
            ...    value=abjad.Markup(r'\bold { over pressure }'),
            ...    )
            >>> override.lilypond_type
            'Staff'

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.lilypond_type is None
            True

        """
        return self._lilypond_type

    @property
    def grob_name(self) -> str:
        r"""
        Gets grob name.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.grob_name
            'Glissando'

        """
        return self._grob_name

    @property
    def once(self) -> typing.Optional[bool]:
        r"""
        Is true when grob override is to be applied only once.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...    lilypond_type='Staff',
            ...    grob_name='TextSpanner',
            ...    once=True,
            ...    property_path=(
            ...        'bound-details',
            ...        'left',
            ...        'text',
            ...        ),
            ...    value=abjad.Markup(r'\bold { over pressure }'),
            ...    )
            >>> bool(override.once)
            True

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> bool(override.once)
            False

        """
        return self._once

    @property
    def is_revert(self) -> typing.Optional[bool]:
        r"""
        Is true if grob override is a grob revert.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> bool(override.is_revert)
            False

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     is_revert=True,
            ...     property_path='style',
            ...     )
            >>> bool(override.is_revert)
            True

        """
        return self._is_revert

    @property
    def override_format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override \override format pieces.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...    lilypond_type='Staff',
            ...    grob_name='TextSpanner',
            ...    once=True,
            ...    property_path=(
            ...        'bound-details',
            ...        'left',
            ...        'text',
            ...        ),
            ...    value=abjad.Markup(r'\bold { over pressure }'),
            ...    )
            >>> for line in override.override_format_pieces:
            ...     line
            ...
            '\\once \\override Staff.TextSpanner.bound-details.left.text = \\markup {'
            '    \\bold'
            '        {'
            '            over'
            '            pressure'
            '        }'
            '    }'

        """
        result = []
        if self.once:
            result.append(r'\once')
        result.append(r'\override')
        result.append(self._override_property_path_string())
        result.append('=')
        string = Scheme.format_embedded_scheme_value(self.value)
        value_pieces = string.split('\n')
        result.append(value_pieces[0])
        result[:] = [' '.join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def override_string(self) -> str:
        r"""
        Gets LilyPond grob override \override string.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.override_string
            "\\override Glissando.style = #'zigzag"

        """
        return '\n'.join(self.override_format_pieces)

    @property
    def property_path(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override property path.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...    lilypond_type='Staff',
            ...    grob_name='TextSpanner',
            ...    once=True,
            ...    property_path=(
            ...        'bound-details',
            ...        'left',
            ...        'text',
            ...        ),
            ...    value=abjad.Markup(r'\bold { over pressure }'),
            ...    )
            >>> override.property_path
            ('bound-details', 'left', 'text')

        """
        return self._property_path

    @property
    def revert_format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond grob override \revert format pieces.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.revert_format_pieces
            ('\\revert Glissando.style',)

        """
        result = rf'\revert {self._revert_property_path_string()}'
        return (result,)

    @property
    def revert_string(self) -> str:
        r"""
        Gets LilyPond grob override \revert string.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.revert_string
            '\\revert Glissando.style'

        """
        return '\n'.join(self.revert_format_pieces)

    @property
    def value(self) -> typing.Any:
        r"""
        Gets value of LilyPond grob override.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...    lilypond_type='Staff',
            ...    grob_name='TextSpanner',
            ...    once=True,
            ...    property_path=(
            ...        'bound-details',
            ...        'left',
            ...        'text',
            ...        ),
            ...    value=abjad.Markup(r'\bold { over pressure }'),
            ...    )
            >>> override.value
            Markup(contents=[MarkupCommand('bold', ['over', 'pressure'])])

        """
        return self._value

    ### PUBLIC METHODS ###

    def tweak_string(self, directed=True, grob=False) -> str:
        r"""
        Gets LilyPond grob override \tweak string.

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='Glissando',
            ...     property_path='style',
            ...     value=abjad.SchemeSymbol('zigzag'),
            ...     )
            >>> override.tweak_string()
            "- \\tweak style #'zigzag"

        ..  container:: example

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='RehearsalMark',
            ...     property_path='color',
            ...     value='red',
            ...     )
            >>> override.tweak_string(directed=False)
            '\\tweak color #red'

        ..  container:: example

            LilyPond literals are allowed:

            >>> override = abjad.LilyPondGrobOverride(
            ...     grob_name='TextSpann',
            ...     property_path=('bound-details', 'left-broken', 'text'),
            ...     value=abjad.LilyPondLiteral(r'\markup \upright pont.'),
            ...     )
            >>> override.tweak_string(directed=False)
            '\\tweak bound-details.left-broken.text \\markup \\upright pont.'

        """
        from abjad.indicators.LilyPondLiteral import LilyPondLiteral
        if directed:
            result = [r'- \tweak']
        else:
            result = [r'\tweak']
        if grob:
            property_path = (self.grob_name,) + self.property_path
        else:
            property_path = self.property_path
        string = '.'.join(property_path)
        result.append(string)
        if isinstance(self.value, LilyPondLiteral):
            assert isinstance(self.value.argument, str)
            string = self.value.argument
        else:
            string = Scheme.format_embedded_scheme_value(self.value)
        result.append(string)
        return ' '.join(result)
