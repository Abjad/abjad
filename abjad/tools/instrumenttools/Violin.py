from abjad.tools.instrumenttools.Instrument import Instrument


class Violin(Instrument):
    r'''Violin.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Violin }
                \set Staff.shortInstrumentName = \markup { Vn. }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name='violin',
        short_name='vn.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        context=None,
        default_tuning=('G3', 'D4', 'A4', 'E5'),
        middle_c_sounding_pitch=None,
        pitch_range='[G3, G7]',
        ):
        import abjad
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True
        self._default_tuning = abjad.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets violin's allowable clefs.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.allowable_clefs
            ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets violin's default tuning.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.default_tuning
            Tuning(pitches=PitchSegment(['g', "d'", "a'", "e''"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of violin's written middle C.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(violin.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets violin's name.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.name
            'violin'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets violin's instrument name markup.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.name_markup
            Markup(contents=['Violin'])

            >>> abjad.show(violin.name_markup) # doctest: +SKIP

        ..  container:: example

            Regression: markup is preserved under new-duplication:

            >>> markup = abjad.Markup('Violin').italic().hcenter_in(12)
            >>> violin_1 = abjad.Violin(
            ...     name_markup=markup,
            ...     )
            >>> abjad.f(violin_1.name_markup)
            \markup {
                \hcenter-in
                    #12
                    \italic
                        Violin
                }

            >>> violin_2 = abjad.new(violin_1)
            >>> abjad.f(violin_2.name_markup)
            \markup {
                \hcenter-in
                    #12
                    \italic
                        Violin
                }

            >>> markup_1 = violin_1.name_markup
            >>> markup_2 = violin_2.name_markup
            >>> markup_1 == markup_2
            True

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets violin's range.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.pitch_range
            PitchRange('[G3, G7]')

            >>> abjad.show(violin.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets violin's short instrument name.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.short_name
            'vn.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets violin's short instrument name markup.

        ..  container:: example

            >>> violin = abjad.Violin()
            >>> violin.short_name_markup
            Markup(contents=['Vn.'])

            >>> abjad.show(violin.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
