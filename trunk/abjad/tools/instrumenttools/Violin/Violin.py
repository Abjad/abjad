# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.StringInstrument import StringInstrument


class Violin(StringInstrument):
    r'''A violin.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> violin = instrumenttools.Violin()
        >>> violin = violin.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Violin }
            \set Staff.shortInstrumentName = \markup { Vn. }
            c'8
            d'8
            e'8
            f'8
        }

    The violin targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        StringInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'violin'
        self._default_performer_names.append('violinist')
        self._default_pitch_range = pitchtools.PitchRange(-5, 43)
        self._default_short_instrument_name = 'vn.'
        self._default_starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._is_primary_instrument = True
