# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Guitar(StringInstrument):
    r'''Abjad model of the guitar:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Guitar()(staff)
        Guitar()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Guitar }
            \set Staff.shortInstrumentName = \markup { Gt. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The guitar targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'guitar'
        self._default_performer_names.append('guitarist')
        self._default_short_instrument_name = 'gt.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('c')
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-20, 16)
