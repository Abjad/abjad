# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Saxophone.Saxophone import Saxophone


class BaritoneSaxophone(Saxophone):
    r'''Abjad model of the baritone saxophone:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.BaritoneSaxophone()(staff)
        BaritoneSaxophone()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone saxophone }
            \set Staff.shortInstrumentName = \markup { Bar. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The baritone saxophone is pitched in E-flat.

    The baritone saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'baritone saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'bar. sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('ef,')
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-24, 8)
