# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.WindInstrument import WindInstrument


class Flute(WindInstrument):
    r'''Abjad model of the flute:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Flute()(staff)
        Flute()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The flute targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        WindInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'flute'
        self._default_performer_names.extend(['flautist', 'flutist'])
        self._default_short_instrument_name = 'fl.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(0, 38)
