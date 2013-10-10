# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class FrenchHorn(Instrument):
    r'''Abjad model of the French horn:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.FrenchHorn()(staff)
        FrenchHorn()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Horn }
            \set Staff.shortInstrumentName = \markup { Hn. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The French horn targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'horn'
        self._default_performer_names.extend([
            'wind player',
            'brass player',
            'hornist',
            ])
        self._default_short_instrument_name = 'hn.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('f')
        self.starting_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-25, 17)
