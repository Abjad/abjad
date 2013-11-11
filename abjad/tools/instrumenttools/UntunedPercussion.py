# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class UntunedPercussion(Instrument):
    r'''An untuned percussion instrument.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> percussion = instrumenttools.UntunedPercussion()
        >>> attach(percussion, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Untuned percussion }
            \set Staff.shortInstrumentName = \markup { Perc. }
            c'8
            d'8
            e'8
            f'8
        }

    Untuned percussion targets the staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'untuned percussion'
        self._default_performer_names.extend([
            'percussionist',
            ])
        self._default_short_instrument_name = 'perc.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [marktools.Clef('percussion')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-48, 39)

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
