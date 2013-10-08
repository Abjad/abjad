# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.BrassInstrument import BrassInstrument


class Trumpet(BrassInstrument):
    r'''Abjad model of the trumpet:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Trumpet()(staff)
        Trumpet()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Trumpet }
            \set Staff.shortInstrumentName = \markup { Tp. }
            c'8
            d'8
            e'8
            f'8
        }

    The trumpet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        BrassInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'trumpet'
        self._default_performer_names.append('trumpeter')
        self._default_short_instrument_name = 'tp.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-6, 26)
