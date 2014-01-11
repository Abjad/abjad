# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class UntunedPercussion(Instrument):
    r'''An untuned percussion instrument.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> untuned_percussion = instrumenttools.UntunedPercussion()
        >>> attach(untuned_percussion, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Untuned percussion }
            \set Staff.shortInstrumentName = \markup { Perc. }
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
        instrument_name='untuned percussion',
        short_instrument_name='perc.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('percussion',),
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._performer_names.extend([
            'percussionist',
            ])

    ### CLASS VARIABLES ###

    known_untuned_percussion = list(sorted(set([
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
        'cuíca',
        'djembe',
        'finger cymbals',
        'flexatone',
        'frame drum',
        'gong',
        'güiro',
        'jawbone',
        'maracas',
        'ratchet',
        'rattle',
        'sand blocks',
        'siren',
        'slapstick',
        'slide whistle',
        'snare drum',
        'steel drums',
        'tambourine',
        'temple blocks',
        'thunder machine',
        'thundersheet',
        'toms',
        'triangle',
        'vibraslap',
        'whistle',
        'wind chime',
        'wind machine',
        'wood block',
        ])))
        
    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets untuned percussion's allowable clefs.

        ..  container:: example

            ::

                >>> untuned_percussion.allowable_clefs
                ClefInventory([Clef(name='percussion')])

            ::

                >>> show(untuned_percussion.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets untuned percussion's name.

        ..  container:: example

            ::

                >>> untuned_percussion.instrument_name
                'untuned percussion'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets untuned percussion's instrument name markup.

        ..  container:: example

            ::

                >>> untuned_percussion.instrument_name_markup
                Markup(('Untuned percussion',))

            ::

                >>> show(untuned_percussion.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets untuned percussion's range.

        ..  container:: example

            ::

                >>> untuned_percussion.pitch_range
                PitchRange('[A0, C8]')

            ::

                >>> show(untuned_percussion.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets untuned_percussion's short instrument name.

        ..  container:: example

            ::

                >>> untuned_percussion.short_instrument_name
                'perc.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets untuned percussion's short instrument name markup.

        ..  container:: example

            ::

                >>> untuned_percussion.short_instrument_name_markup
                Markup(('Perc.',))

            ::

                >>> show(untuned_percussion.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of untuned percussion's written middle C.

        ..  container:: example

            ::

                >>> untuned_percussion.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(untuned_percussion.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
