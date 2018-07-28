import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.markups import Markup
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.top.new import new


class MarginMarkup(AbjadValueObject):
    r"""
    Margin markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=abjad.Markup('Vc.'),
        ...     )
        >>> abjad.attach(margin_markup, staff[0])
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName =
                \markup { Vc. }
                \set Staff.shortInstrumentName =
                \markup { Vc. }
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

    _latent = True

    _parameter = True

    _publish_storage_format = True

    _redraw = True

    ### INITIALIZER ##

    def __init__(
        self,
        *,
        context: str = 'Staff',
        format_slot: str = 'before',
        markup: Markup = None,
        ) -> None:
        self._context = context
        self._format_slot = format_slot
        self._markup = markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is margin markup with context and markup
        equal to those of this margin markup.

        ..  container:: example

            >>> margin_markup_1 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_2 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_3 = abjad.MarginMarkup(
            ...     context='Staff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )

            >>> margin_markup_1 == margin_markup_1
            True
            >>> margin_markup_1 == margin_markup_2
            True
            >>> margin_markup_1 == margin_markup_3
            False

            >>> margin_markup_2 == margin_markup_1
            True
            >>> margin_markup_2 == margin_markup_2
            True
            >>> margin_markup_2 == margin_markup_3
            False

            >>> margin_markup_3 == margin_markup_1
            False
            >>> margin_markup_3 == margin_markup_2
            False
            >>> margin_markup_3 == margin_markup_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if self.context == argument.context and self.markup == argument.markup:
            return True
        return False

    def __hash__(self) -> int:
        r"""Hashes margin markup.

        Redefined in tandem with __eq__.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Hp.'),
            ...     )

            >>> hash_ = hash(margin_markup)
            >>> isinstance(hash_, int)
            True

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
        result.append(rf'\set {context!s}.shortInstrumentName =')
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
        Gets default context of margin markup.

        ..  container:: example

            >>> abjad.MarginMarkup().context
            'Staff'

        """
        return self._context

    @property
    def format_slot(self) -> str:
        """
        Gets format slot.

        ..  container:: example

            >>> abjad.MarginMarkup().format_slot
            'before'

        """
        return self._format_slot

    @property
    def latent(self) -> bool:
        """Is true.

        ..  container::

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.latent
            True

        Class constant.
        """
        return self._latent

    @property
    def markup(self) -> typing.Optional[Markup]:
        """
        Gets (instrument name) markup.
        """
        return self._markup

    @property
    def parameter(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.parameter
            True

        Class constant.
        """
        return self._parameter

    @property
    def redraw(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Vc.'),
            ...     )
            >>> margin_markup.redraw
            True

        Class constant.
        """
        return self._redraw

    @property
    def tweaks(self) -> None:
        """
        Are not implemented on margin markup.
        
        The LilyPond ``\shortInstrumentName`` command refuses tweaks.

        Craft explicit markup instead.
        """
        pass
