from .Instrument import Instrument


class Percussion(Instrument):
    r'''Percussion instrument.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> percussion = abjad.Percussion()
        >>> abjad.attach(percussion, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Percussion }
                \set Staff.shortInstrumentName = \markup { Perc. }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    known_percussion = list(sorted(set([
        'agogô',
        'anvil',
        'bass drum',
        'bongo drums',
        'cabasa',
        'cajón',
        'castanets',
        'caxixi',
        'claves',
        'conga drums',
        'cowbell',
        'crotales',
        'cuíca',
        'djembe',
        'finger cymbals',
        'flexatone',
        'frame drum',
        'gong',
        'güiro',
        'hand-held stones',
        'jawbone',
        'maracas',
        'ratchet',
        'rattle',
        'sand blocks',
        'scraped slate',
        'siren',
        'slapstick',
        'slide whistle',
        'snare drum',
        'sponges',
        'suspended cymbal',
        'steel drums',
        'tam-tam',
        'tambourine',
        'temple blocks',
        'thunder machine',
        'thundersheet',
        'toms',
        'tubular bells',
        'triangle',
        'vibraslap',
        'whistle',
        'wind chime',
        'wind machine',
        'wood blocks',
        'wood planks',
        ])))

    ### INITIALIZER ###

    def __init__(
        self,
        name='percussion',
        short_name='perc.',
        markup=None,
        short_markup=None,
        allowable_clefs=('percussion',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range=None,
        hide=None,
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            hide=hide,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets percussion's allowable clefs.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.allowable_clefs
            ('percussion',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets percussion's instrument name markup.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.markup
            Markup(contents=['Percussion'])

            >>> abjad.show(percussion.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of percussion's written middle C.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(percussion.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets percussion's name.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.name
            'percussion'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets percussion's range.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.pitch_range
            PitchRange('[A0, C8]')

            >>> abjad.show(percussion.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets percussion's short instrument name markup.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.short_markup
            Markup(contents=['Perc.'])

            >>> abjad.show(percussion.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets percussion's short instrument name.

        ..  container:: example

            >>> percussion = abjad.Percussion()
            >>> percussion.short_name
            'perc.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
