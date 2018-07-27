from abjad.system.AbjadObject import AbjadObject
from abjad.core.Context import Context
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
import typing


class PersistentOverride(AbjadObject):
    """
    Persistent override.

    ..  container:: example

        >>> override = abjad.PersistentOverride(
        ...     attribute='bar_extent',
        ...     context='Staff',
        ...     grob='bar_line',
        ...     value=(-2, 0),
        ...     )

        >>> abjad.f(override)
        abjad.PersistentOverride(
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            value=(-2, 0),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_after',
        '_attribute',
        '_context',
        '_grob',
        '_hide',
        '_value',
        )

    _parameter = True
    
    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        after: bool = None,
        attribute: str = None,
        context: str = None,
        grob: str = None,
        hide: bool = None,
        value: typing.Any = None,
        ) -> None:
        if after is not None:
            after = bool(after)
        self._after = after
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is persistent override with attribute,
        context, grob, value equal to those of this persistent override.

        ..  container:: example

            >>> override_1 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_2 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_3 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Score',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override_1 == override_1
            True
            >>> override_1 == override_2
            True
            >>> override_1 == override_3
            False

            >>> override_2 == override_1
            True
            >>> override_2 == override_2
            True
            >>> override_2 == override_3
            False

            >>> override_3 == override_1
            False
            >>> override_3 == override_2
            False
            >>> override_3 == override_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if (self.attribute == argument.attribute and
            self.context == argument.context and
            self.grob == argument.grob and
            self.value == argument.value):
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes persistent override.
        """
        return super().__hash__()

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self, context=None):
        if isinstance(context, Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        strings = []
        string = LilyPondFormatManager.make_lilypond_override_string(
            self.grob,
            self.attribute,
            self.value,
            context=lilypond_type,
            once=False,
            )
        strings.append(string)
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.hide:
            return bundle
        #staff = abjad.inspect(component).parentage().get_first(abjad.Staff)
        #strings = self._get_lilypond_format(context=staff)
        strings = self._get_lilypond_format()
        bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def after(self) -> typing.Optional[bool]:
        """
        Is true when override formats after leaf.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.after is None
            True

        """
        return self._after

    @property
    def attribute(self) -> typing.Optional[str]:
        """
        Gets attribute.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.attribute
            'bar_extent'

        """
        return self._attribute

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.context
            'Staff'

        """
        return self._context

    @property
    def grob(self) -> typing.Optional[str]:
        """
        Gets grob.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.grob
            'bar_line'

        """
        return self._grob

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when staff lines should not appear in output.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.hide is None
            True

        """
        return self._hide

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.parameter
            True

        Class constant.
        """
        return self._parameter

    @property
    def value(self) -> typing.Optional[str]:
        """
        Gets value.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.value
            (-2, 0)

        """
        return self._value
