# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassClarinet(Instrument):
    r'''A bass clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> bass_clarinet = instrumenttools.BassClarinet()
        >>> bass_clarinet = attach(bass_clarinet, staff)
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
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('bf,')
        self._default_allowable_clefs = marktools.ClefInventory([
            marktools.Clef('treble'), 
            marktools.Clef('bass'),
            ])
        self._default_instrument_name = 'bass clarinet'
        self._default_pitch_range = pitchtools.PitchRange(-26, 19)
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._default_short_instrument_name = 'bass cl.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = marktools.ClefInventory([
            marktools.Clef('treble'),
            ])
        self._is_primary_instrument = False

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> bass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('bf,')

            ::

                >>> bass_clarinet.sounding_pitch_of_written_middle_c = 'b,'
                >>> bass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('b,')

            :: 

                >>> bass_clarinet.sounding_pitch_of_written_middle_c = None
                >>> bass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('bf,')

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
