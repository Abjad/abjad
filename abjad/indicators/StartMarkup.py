import typing

from ..bundle import LilyPondFormatBundle
from ..markups import Markup
from ..new import new
from ..storage import StorageFormatManager


class StartMarkup:
    r"""
    Start markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> start_markup = abjad.StartMarkup(markup=abjad.Markup('Cellos'))
        >>> abjad.attach(start_markup, staff[0])
        >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                \set Staff.instrumentName =
                \markup { Cellos }
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Set instrument name to custom-defined LilyPond function like this:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> start_markup = abjad.StartMarkup(markup=r'\my_instrument_name')
        >>> abjad.attach(start_markup, staff[0])

        >>> string = abjad.lilypond(staff)
        >>> print(string)
        \new Staff
        {
            \set Staff.instrumentName = \my_instrument_name
            c'4
            d'4
            e'4
            f'4
        }

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_context", "_format_slot", "_markup")

    ### INITIALIZER ##

    def __init__(
        self,
        markup: typing.Union[str, Markup] = "instrument name",
        *,
        context: str = "Staff",
        format_slot: str = "before",
    ) -> None:
        assert isinstance(context, str), repr(context)
        self._context = context
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot
        if markup is not None:
            assert isinstance(markup, (str, Markup)), repr(markup)
        self._markup = markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is start markup with context and markup
        equal to those of this start markup.

        ..  container:: example

            >>> start_markup_1 = abjad.StartMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     )
            >>> start_markup_2 = abjad.StartMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     )
            >>> start_markup_3 = abjad.StartMarkup(
            ...     context='Staff',
            ...     markup=abjad.Markup('Harp'),
            ...     )

            >>> start_markup_1 == start_markup_1
            True
            >>> start_markup_1 == start_markup_2
            True
            >>> start_markup_1 == start_markup_3
            False

            >>> start_markup_2 == start_markup_1
            True
            >>> start_markup_2 == start_markup_2
            True
            >>> start_markup_2 == start_markup_3
            False

            >>> start_markup_3 == start_markup_1
            False
            >>> start_markup_3 == start_markup_2
            False
            >>> start_markup_3 == start_markup_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if self.context == argument.context and self.markup == argument.markup:
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes start markup.

        ..  container:: example

            >>> start_markup = abjad.StartMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     )

            >>> hash_ = hash(start_markup)
            >>> isinstance(hash_, int)
            True

        Redefined in tandem with __eq__.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_type(self):
        if isinstance(self.context, type):
            return self.context.__name__
        elif isinstance(self.context, str):
            return self.context
        else:
            return type(self.context).__name__

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self, context=None):
        result = []
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        if isinstance(self.markup, Markup):
            markup = self.markup
            if markup.direction is not None:
                markup = new(markup, direction=None)
            pieces = markup._get_format_pieces()
            result.append(rf"\set {context!s}.instrumentName =")
            result.extend(pieces)
        else:
            assert isinstance(self.markup, str)
            string = rf"\set {context!s}.instrumentName = {self.markup}"
            result.append(string)
        return result

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        """
        Gets default context of start markup.

        ..  container:: example

            >>> start_markup = abjad.StartMarkup(markup=abjad.Markup('Cellos'))
            >>> start_markup.context
            'Staff'

        """
        return self._context

    @property
    def format_slot(self) -> str:
        """
        Gets format slot.

        ..  container:: example

            >>> start_markup = abjad.StartMarkup(markup=abjad.Markup('Cellos'))
            >>> start_markup.format_slot
            'before'

        """
        return self._format_slot

    @property
    def markup(self) -> typing.Union[str, Markup]:
        """
        Gets (instrument name) markup.

        ..  container:: example

            >>> start_markup = abjad.StartMarkup(markup=abjad.Markup('Cellos'))
            >>> start_markup.markup
            Markup(contents=['Cellos'])

        """
        return self._markup

    @property
    def tweaks(self) -> None:
        r"""
        Are not implemented on start markup.

        The LilyPond ``\instrumentName`` command refuses tweaks.

        Craft explicit markup instead.
        """
        pass
