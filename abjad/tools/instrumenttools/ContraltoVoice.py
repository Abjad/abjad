# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContraltoVoice(Instrument):
    r'''A contralto voice.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contralto = instrumenttools.ContraltoVoice()
        >>> attach(contralto, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contralto voice }
            \set Staff.shortInstrumentName = \markup { Contralto }
            c'8
            d'8
            e'8
            f'8
        }

    The contralto voice targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    default_performer_abbreviation = 'contr.'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contralto voice'
        self._default_performer_names.extend([
            'vocalist',
            'contralto',
            ])
        self._default_short_instrument_name = 'contralto'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [marktools.Clef('treble')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(('F3', 'G5'))
