from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.markuptools.Markup import Markup


class MarginMarkup(AbjadValueObject):
    r'''Margin markup.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> margin_markup = abjad.MarginMarkup(
        ...     markup=abjad.Markup('Cello'),
        ...     short_markup=abjad.Markup('Vc.')
        ...     )
        >>> abjad.attach(margin_markup, staff[0])
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.instrumentName = \markup { Cello }
                \set Staff.shortInstrumentName = \markup { Vc. }
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
        '_short_markup',
        )

    _latent = True

    _persistent = True

    _publish_storage_format = True

    _redraw = True

    ### INITIALIZER ##

    def __init__(
        self,
        context: str = 'Staff',
        format_slot: str = 'before',
        markup: Markup = None,
        short_markup: Markup = None,
        ) -> None:
        self._context: str = context
        self._format_slot: str = format_slot
        self._markup: Markup = markup
        self._short_markup: Markup = short_markup

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is margin markup with context, markup and
        short markup equal to those of this margin markup.

        ..  container:: example

            >>> margin_markup_1 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_2 = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )
            >>> margin_markup_3 = abjad.MarginMarkup(
            ...     context='Staff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
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

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        if (self.context == argument.context and
            self.markup == argument.markup and
            self.short_markup == argument.short_markup):
            return True
        return False

    def __hash__(self):
        r'''Hashes margin markup.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     context='PianoStaff',
            ...     markup=abjad.Markup('Harp'),
            ...     short_markup=abjad.Markup('Hp.'),
            ...     )

            >>> hash_ = hash(margin_markup)
            >>> isinstance(hash_, int)
            True

        Returns integer.
        '''
        return super(MarginMarkup, self).__hash__()

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
        first_line = r'\set {!s}.instrumentName = {!s}'
        first_line = first_line.format(context, pieces[0])
        result.append(first_line)
        result.extend(pieces[1:])
        short_markup = self.short_markup
        if short_markup.direction is not None:
            short_markup = abjad.new(
                short_markup,
                direction=None,
                )
        pieces = short_markup._get_format_pieces()
        first_line = r'\set {!s}.shortInstrumentName = {!s}'
        first_line = first_line.format(context, pieces[0])
        result.append(first_line)
        result.extend(pieces[1:])
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
        r'''Gets default context of margin markup.

        ..  container:: example

            >>> abjad.MarginMarkup().context
            'Staff'

        Returns string.
        '''
        return self._context

    @property
    def format_slot(self):
        r'''Gets format slot.

        ..  container:: example

            >>> abjad.MarginMarkup().format_slot
            'before'

        Returns string.
        '''
        return self._format_slot

    @property
    def latent(self):
        r'''Is true.

        ..  container::

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Cello'),
            ...     short_markup=abjad.Markup('Vc.')
            ...     )
            >>> margin_markup.latent
            True

        Class constant.

        Returns true.
        '''
        return self._latent

    @property
    def markup(self):
        r'''Gets (instrument name) markup.

        Returns markup.
        '''
        return self._markup

    @property
    def persistent(self):
        r'''Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Cello'),
            ...     short_markup=abjad.Markup('Vc.')
            ...     )
            >>> margin_markup.persistent
            True

        Class constant.

        Returns true.
        '''
        return self._persistent

    @property
    def redraw(self):
        r'''Is true.

        ..  container:: example

            >>> margin_markup = abjad.MarginMarkup(
            ...     markup=abjad.Markup('Cello'),
            ...     short_markup=abjad.Markup('Vc.')
            ...     )
            >>> margin_markup.redraw
            True

        Class constant.

        Returns true.
        '''
        return self._redraw

    @property
    def short_markup(self):
        r'''Gets short (instrument name) markup.

        Returns markup.
        '''
        return self._short_markup
