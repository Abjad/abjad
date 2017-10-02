from abjad.tools.instrumenttools.Instrument import Instrument


class Xylophone(Instrument):
    r'''Xylphone.

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> xylophone = abjad.Xylophone()
            >>> abjad.attach(xylophone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Xylophone }
                \set Staff.shortInstrumentName = \markup { Xyl. }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        name='xylophone',
        short_name='xyl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        default_scope=None,
        middle_c_sounding_pitch='C5',
        pitch_range='[C4, C7]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            default_scope=default_scope,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets xylophone's allowable clefs.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.allowable_clefs
                ('treble',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of xylophone's written middle C.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.middle_c_sounding_pitch
                NamedPitch("c''")

            ::

                >>> show(xylophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets xylophone's name.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.name
                'xylophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets xylophone's instrument name markup.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.name_markup
                Markup(contents=['Xylophone'])

            ::

                >>> show(xylophone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets xylophone's range.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.pitch_range
                PitchRange('[C4, C7]')

            ::

                >>> show(xylophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets xylophone's short instrument name.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.short_name
                'xyl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets xylophone's short instrument name markup.

        ..  container:: example

            ::

                >>> xylophone = abjad.Xylophone()
                >>> xylophone.short_name_markup
                Markup(contents=['Xyl.'])

            ::

                >>> show(xylophone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
