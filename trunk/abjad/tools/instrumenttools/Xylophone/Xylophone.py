# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.PercussionInstrument \
	import PercussionInstrument


class Xylophone(PercussionInstrument):
    r'''Abjad model of the xylphone:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> instrumenttools.Xylophone()(staff)
        Xylophone()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Xylophone }
            \set Staff.shortInstrumentName = \markup { Xyl. }
            c'8
            d'8
            e'8
            f'8
        }

    The xylophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        PercussionInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'xylophone'
        self._default_performer_names.append('xylophonist')
        self._default_short_instrument_name = 'xyl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch("c''")
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(0, 36)
