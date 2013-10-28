# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorVoice(Instrument):
    r'''A tenor voice.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> tenor = instrumenttools.TenorVoice()
        >>> tenor.attach(staff)
        TenorVoice()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Tenor voice }
            \set Staff.shortInstrumentName = \markup { Tenor }
            c'8
            d'8
            e'8
            f'8
        }

    The tenor voice targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    default_performer_abbreviation = 'ten.'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'tenor voice'
        self._default_performer_names.extend([
            'vocalist',
            'tenor',
            ])
        self._default_short_instrument_name = 'tenor'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange('C3', 'D5')
        #self._make_default_name_markups()
