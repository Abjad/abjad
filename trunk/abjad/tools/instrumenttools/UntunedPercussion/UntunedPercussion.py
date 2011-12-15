# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._PercussionInstrument import _PercussionInstrument


class UntunedPercussion(_PercussionInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of untuned percussion::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.UntunedPercussion()(staff)
        UntunedPercussion()(Staff{4})

    ::

        abjad> f(staff)
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

    def __init__(self, instrument_name=None, short_instrument_name=None,
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        _PercussionInstrument.__init__(self, instrument_name=instrument_name, 
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup, 
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'untuned percussion'
        self._default_short_instrument_name = 'perc.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('percussion')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-48, 39)

    ### CLASS ATTRIBUTES ###

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
