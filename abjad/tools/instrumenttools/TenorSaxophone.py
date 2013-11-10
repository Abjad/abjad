# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorSaxophone(Instrument):
    r'''A tenor saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> sax = instrumenttools.TenorSaxophone()
        >>> attach(sax, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Tenor saxophone }
            \set Staff.shortInstrumentName = \markup { Ten. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The tenor saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'tenor saxophone'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._default_short_instrument_name = 'ten. sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('bf,')
        self._starting_clefs = [marktools.Clef('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-16, 16)
        #self._make_default_name_markups()
