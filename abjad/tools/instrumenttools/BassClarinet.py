# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassClarinet(Instrument):
    r'''A bass clarinet.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> bass_clarinet = instrumenttools.BassClarinet()
        >>> attach(bass_clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
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

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bass clarinet',
        short_instrument_name='bass cl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='bf,',
        ):
        pitch_range = pitch_range = pitchtools.PitchRange(-26, 19)
        allowable_clefs = indicatortools.ClefInventory(['treble', 'bass'])
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'clarinettist',
            'clarinetist',
            ])
        self._starting_clefs = indicatortools.ClefInventory(['treble'])

#    ### PUBLIC PROPERTIES ###
#
#    @property
#    def sounding_pitch_of_written_middle_c(self):
#        r'''Gets and sets sounding pitch of written middle C.
#
#        ::
#
#            >>> bass_clarinet.sounding_pitch_of_written_middle_c
#            NamedPitch('bf,')
#
#        ::
#
#            >>> bass_clarinet.sounding_pitch_of_written_middle_c = 'b,'
#            >>> bass_clarinet.sounding_pitch_of_written_middle_c
#            NamedPitch('b,')
#
#        :: 
#
#            >>> bass_clarinet.sounding_pitch_of_written_middle_c = None
#            >>> bass_clarinet.sounding_pitch_of_written_middle_c
#            NamedPitch('bf,')
#
#        Returns named pitch.
#        '''
#        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
#
#    @sounding_pitch_of_written_middle_c.setter
#    def sounding_pitch_of_written_middle_c(self, pitch):
#        Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
