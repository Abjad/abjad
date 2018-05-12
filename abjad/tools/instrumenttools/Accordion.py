from .Instrument import Instrument


class Accordion(Instrument):
    r'''Accordion.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> accordion = abjad.Accordion()
        >>> abjad.attach(accordion, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
            \new PianoStaff
            <<
                \new Staff
                {
                    \set PianoStaff.instrumentName = \markup { Accordion }
                    \set PianoStaff.shortInstrumentName = \markup { Acc. }
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
                    \clef "bass"
                    c'2
                    b2
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name='accordion',
        short_name='acc.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[E1, C8]',
        hide=None,
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            hide=hide,
            )
        self._context = context
        self._is_primary_instrument = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats accordion.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> abjad.f(accordion)
            abjad.Accordion(
                name='accordion',
                short_name='acc.',
                markup=abjad.Markup(
                    contents=['Accordion'],
                    ),
                short_markup=abjad.Markup(
                    contents=['Acc.'],
                    ),
                allowable_clefs=('treble', 'bass'),
                context='StaffGroup',
                middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                pitch_range=abjad.PitchRange('[E1, C8]'),
                )

        Returns string.
        '''
        superclass = super(Accordion, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets accordion's allowable clefs.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.allowable_clefs
            ('treble', 'bass')

        Returns tuple.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def context(self):
        r'''Gets (historically conventional) context.

        ..  container:: example

            >>> abjad.Accordion().context
            'StaffGroup'

        Returns ``'StaffGroup'``.

        Override with ``abjad.attach(..., context='...')``.
        '''
        return self._context

    @property
    def markup(self):
        r'''Gets accordion's instrument name markup.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.markup
            Markup(contents=['Accordion'])

            >>> abjad.show(accordion.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of accordion's written middle C.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(accordion.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets accordion's name.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.name
            'accordion'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets accordion's range.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.pitch_range
            PitchRange('[E1, C8]')

            >>> abjad.show(accordion.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets accordion's short instrument name markup.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.short_markup
            Markup(contents=['Acc.'])

            >>> abjad.show(accordion.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets accordion's short instrument name.

        ..  container:: example

            >>> accordion = abjad.Accordion()
            >>> accordion.short_name
            'acc.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
