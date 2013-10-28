# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassClarinet(Instrument):
    r'''A contrassbass clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clarinet = instrumenttools.ContrabassClarinet()
        >>> clarinet.attach(staff)
        ContrabassClarinet()(Staff{4})
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass clarinet }
            \set Staff.shortInstrumentName = \markup { Cbass cl. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass clarinet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'contrabass clarinet'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._default_short_instrument_name = 'cbass cl.'
        self._is_primary_instrument = False
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch('bf,,')
        self._starting_clefs = [contexttools.ClefMark('treble')]
        self.allowable_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._default_pitch_range = pitchtools.PitchRange(-38, 7)
