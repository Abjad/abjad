from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.markuptools.Markup import Markup


class StartMarkup(AbjadValueObject):
    r'''Start markup.

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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_context',
        '_format_slot',
        '_markup',
        )

    _publish_storage_format = True

    ### INITIALIZER ##

    def __init__(
        self,
        context: str = 'Staff',
        format_slot: str = 'before',
        markup: Markup = None,
        ) -> None:
        self._context: str = context
        self._format_slot: str = format_slot
        self._markup: Markup = markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is start markup with context and markup
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

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        if self.context == argument.context and self.markup == argument.markup:
            return True
        return False

    def __hash__(self):
        r'''Hashes start markup.

        ..  container:: example

            >>> start_markup = abjad.StartMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     )

            >>> hash_ = hash(start_markup)
            >>> isinstance(hash_, int)
            True

        Returns integer.
        '''
        return super(StartMarkup, self).__hash__()

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
        import abjad
        result = []
        markup = self.markup
        if markup.direction is not None:
            markup = abjad.new(
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
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.extend(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of start markup.

        ..  container:: example

            >>> abjad.StartMarkup().context
            'Staff'

        Returns string.
        '''
        return self._context

    @property
    def format_slot(self):
        r'''Gets format slot.

        ..  container:: example

            >>> abjad.StartMarkup().format_slot
            'before'

        Returns string.
        '''
        return self._format_slot

    @property
    def markup(self):
        r'''Gets (instrument name) markup.

        Returns markup.
        '''
        return self._markup
