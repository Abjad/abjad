# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class UntunedPercussion(Instrument):
    r'''An untuned percussion instrument.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> percussion = instrumenttools.UntunedPercussion()
        >>> attach(percussion, staff)
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
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        allowable_clefs = allowable_clefs or indicatortools.ClefInventory(
            ['percussion'])
        pitch_range = pitch_range or pitchtools.PitchRange(-48, 39)
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
        self._starting_clefs = indicatortools.ClefInventory(['percussion'])

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
