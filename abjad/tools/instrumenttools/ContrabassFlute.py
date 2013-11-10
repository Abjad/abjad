# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassFlute(Instrument):
    r'''A contrabass flute.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contrabass_flute = instrumenttools.ContrabassFlute()
        >>> attach(contrabass_flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass flute }
            \set Staff.shortInstrumentName = \markup { Cbass. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass flute targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass flute'
        self._default_performer_names.extend([
            'wind player',
            'flautist',
            'flutist',
            ])
        self._default_short_instrument_name = 'cbass. fl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('g,')
        self._default_pitch_range = pitchtools.PitchRange(-17, 19)
