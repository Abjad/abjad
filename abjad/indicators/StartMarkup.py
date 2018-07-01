import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.markups import Markup
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.top.new import new


class StartMarkup(AbjadValueObject):
    r"""
    Start markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> start_markup = abjad.StartMarkup(markup=abjad.Markup('Cellos'))
        >>> abjad.attach(start_markup, staff[0])
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName =
                \markup { Cellos }
                c'4
                d'4
                e'4
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_format_slot',
        '_markup',
        )

    _publish_storage_format = True

    ### INITIALIZER ##

    def __init__(
        self,
        markup: typing.Union[str, Markup] = 'instrument name',
        *,
        context: str = 'Staff',
        format_slot: str = 'before',
        ) -> None:
        assert isinstance(context, str), repr(context)
        self._context = context
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot
        if isinstance(markup, str):
            markup = Markup(markup)
        assert isinstance(markup, Markup), repr(markup)
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
        return super().__hash__()

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
        markup = self.markup
        if markup.direction is not None:
            markup = new(
                markup,
                direction=None,
                )
        if isinstance(context, str):
            pass
        elif context is not None:
            context = context.lilypond_type
        else:
            context = self._lilypond_type
        pieces = markup._get_format_pieces()
        result.append(rf'\set {context!s}.instrumentName =')
        result.extend(pieces)
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

            >>> abjad.StartMarkup().context
            'Staff'

        """
        return self._context

    @property
    def format_slot(self) -> str:
        """
        Gets format slot.

        ..  container:: example

            >>> abjad.StartMarkup().format_slot
            'before'

        """
        return self._format_slot

    @property
    def markup(self) -> Markup:
        """
        Gets (instrument name) markup.

        ..  container:: example

            >>> abjad.StartMarkup().markup
            Markup(contents=['instrument name'])

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
