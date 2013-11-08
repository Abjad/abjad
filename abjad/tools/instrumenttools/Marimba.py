# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Marimba(Instrument):
    r'''A marimba.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> marimba = instrumenttools.Marimba()
        >>> attach(marimba, staff)
        Marimba()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Marimba }
            \set Staff.shortInstrumentName = \markup { Mb. }
            c'8
            d'8
            e'8
            f'8
        }

    The marimba targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'marimba'
        self._default_performer_names.extend([
            'percussionist',
            ])
        self._default_short_instrument_name = 'mb.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self._starting_clefs = [
            marktools.Clef('treble'), marktools.Clef('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-19, 36)
