# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Clarinet.Clarinet import Clarinet


class BassClarinet(Clarinet):
    r'''A bass clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> bass_clarinet = instrumenttools.BassClarinet()
        >>> bass_clarinet = bass_clarinet.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass clarinet }
            \set Staff.shortInstrumentName = \markup { Bass cl. }
            c'8
            d'8
            e'8
            f'8
        }

    The bass clarinet targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Clarinet.__init__(self, **kwargs)
        self._default_instrument_name = 'bass clarinet'
        self._default_short_instrument_name = 'bass cl.'
        self._is_primary_instrument = False
        self._sounding_pitch_of_written_middle_c = pitchtools.NamedPitch('bf,')
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self.allowable_clefs = [
            contexttools.ClefMark('treble'), 
            contexttools.ClefMark('bass'),
            ]
        self._default_pitch_range = pitchtools.PitchRange(-26, 19)

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> bass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('bf,')

            ::

                >>> bass_clarinet.sounding_pitch_of_written_middle_c = 'c'
                >>> bass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            Returns named pitch.
            '''
            return Clarinet.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Clarinet.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
