import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.scheme import Scheme
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class LilyPondContextSetting(AbjadValueObject):
    r"""
    LilyPond context setting.

    ..  container:: example

        >>> context_setting = abjad.LilyPondContextSetting(
        ...    lilypond_type='Score',
        ...    context_property='autoBeaming',
        ...    value=False,
        ...    )

        >>> print('\n'.join(context_setting.format_pieces))
        \set Score.autoBeaming = ##f

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_property',
        '_lilypond_type',
        '_is_unset',
        '_value',
        )

    _format_leaf_children = False

    ### INITIALIZER ###

    def __init__(
        self,
        lilypond_type: str = None,
        context_property: str = 'autoBeaming',
        is_unset: bool = False,
        value: typing.Any = False,
        ) -> None:
        if lilypond_type is not None:
            lilypond_type = str(lilypond_type)
        self._lilypond_type = lilypond_type
        assert isinstance(context_property, str) and context_property
        self._context_property = context_property
        if is_unset is not None:
            is_unset = bool(is_unset)
        self._is_unset = is_unset
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a LilyPond context setting with
        equivalent keyword values.
        """
        return super().__eq__(argument)

    def __hash__(self) -> int:
        """
        Hashes LilyPond context setting.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = '\n'.join(self.format_pieces)
        bundle.context_settings.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_type(self) -> typing.Optional[str]:
        """
        Gets LilyPond type.
        """
        return self._lilypond_type

    @property
    def context_property(self) -> str:
        """
        Gets LilyPond context property name.
        """
        return self._context_property

    @property
    def format_pieces(self) -> typing.Tuple[str, ...]:
        r"""
        Gets LilyPond context setting ``\set`` or ``\unset`` format pieces.
        """
        result = []
        if not self.is_unset:
            result.append(r'\set')
        else:
            result.append(r'\unset')
        if self.lilypond_type is not None:
            string = f'{self.lilypond_type}.{self.context_property}'
            result.append(string)
        else:
            result.append(self.context_property)
        result.append('=')
        string = Scheme.format_embedded_scheme_value(self.value)
        value_pieces = string.split('\n')
        result.append(value_pieces[0])
        result[:] = [' '.join(result)]
        result.extend(value_pieces[1:])
        return tuple(result)

    @property
    def is_unset(self) -> typing.Optional[bool]:
        """
        Is true if context setting unsets its value.
        """
        return self._is_unset

    @property
    def value(self) -> typing.Any:
        """
        Gets value of LilyPond context setting.
        """
        return self._value
