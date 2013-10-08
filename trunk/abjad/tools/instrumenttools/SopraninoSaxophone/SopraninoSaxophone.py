# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Saxophone.Saxophone import Saxophone


class SopraninoSaxophone(Saxophone):
    r'''Abjad model of the sopranino saxophone:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.SopraninoSaxophone()(staff)
        SopraninoSaxophone()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Sopranino saxophone }
            \set Staff.shortInstrumentName = \markup { Sopranino sax. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The sopranino saxophone is pitched in E-flat.

    The sopranino saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'sopranino saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'sopranino sax.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("ef'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self._default_pitch_range = pitchtools.PitchRange(1, 30)
