# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.DoubleReedInstrument \
    import DoubleReedInstrument


class Bassoon(DoubleReedInstrument):
    r'''Abjad model of the bassoon:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contexttools.ClefMark('bass')(staff)
        ClefMark('bass')(Staff{4})

    ::

        >>> instrumenttools.Bassoon()(staff)
        Bassoon()(Staff{4})

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bassoon }
            \set Staff.shortInstrumentName = \markup { Bsn. }
            c'8
            d'8
            e'8
            f'8
        }

    ::

        >>> show(staff) # doctest: +SKIP

    The bassoon targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        DoubleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'bassoon'
        self._default_performer_names.append('bassoonist')
        self._default_short_instrument_name = 'bsn.'
        self._is_primary_instrument = True
        self.primary_clefs = [contexttools.ClefMark('bass')]
        self.all_clefs = [
            contexttools.ClefMark('bass'), contexttools.ClefMark('tenor')]
        self._default_pitch_range = pitchtools.PitchRange(-26, 15)
