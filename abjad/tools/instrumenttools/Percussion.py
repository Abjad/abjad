# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Percussion(Instrument):
    r'''Percussion instrument.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> percussion = abjad.instrumenttools.Percussion()
            >>> abjad.attach(percussion, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
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

    __slots__ = (
        )

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
        instrument_name='percussion',
        short_instrument_name='perc.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('percussion',),
        pitch_range=None,
        middle_c_sounding_pitch=None,
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            middle_c_sounding_pitch=\
                middle_c_sounding_pitch,
            )
        self._performer_names.extend([
            'percussionist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets percussion's allowable clefs.

        ..  container:: example

            ::

                >>> percussion.allowable_clefs
                ClefList([Clef(name='percussion')])

            ::

                >>> show(percussion.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets percussion's name.

        ..  container:: example

            ::

                >>> percussion.instrument_name
                'percussion'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets percussion's instrument name markup.

        ..  container:: example

            ::

                >>> percussion.instrument_name_markup
                Markup(contents=['Percussion'])

            ::

                >>> show(percussion.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets percussion's range.

        ..  container:: example

            ::

                >>> percussion.pitch_range
                PitchRange('[A0, C8]')

            ::

                >>> show(percussion.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets percussion's short instrument name.

        ..  container:: example

            ::

                >>> percussion.short_instrument_name
                'perc.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets percussion's short instrument name markup.

        ..  container:: example

            ::

                >>> percussion.short_instrument_name_markup
                Markup(contents=['Perc.'])

            ::

                >>> show(percussion.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of percussion's written middle C.

        ..  container:: example

            ::

                >>> percussion.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(percussion.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)
