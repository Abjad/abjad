# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassFlute(Instrument):
    r'''A bass flute.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> bass_flute = instrumenttools.BassFlute()
        >>> attach(bass_flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Bass flute }
            \set Staff.shortInstrumentName = \markup { Bass fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The bass flute targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bass flute',
        short_instrument_name='bass fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='c',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-12, 24)
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
            'flautist',
            'flutist',
            ])

#    ### PUBLIC PROPERTIES ###
#
#    @property
#    def sounding_pitch_of_written_middle_c(self):
#        r'''Gets and sets sounding pitch of written middle C.
#
#        ::
#
#            >>> bass_flute.sounding_pitch_of_written_middle_c
#            NamedPitch('c')
#
#        ::
#
#            >>> bass_flute.sounding_pitch_of_written_middle_c = 'cs'
#            >>> bass_flute.sounding_pitch_of_written_middle_c
#            NamedPitch('cs')
#
#        ::
#
#            >>> bass_flute.sounding_pitch_of_written_middle_c = None
#            >>> bass_flute.sounding_pitch_of_written_middle_c
#            NamedPitch('c')
#
#        Returns named pitch.
#        '''
#        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
#
#    @sounding_pitch_of_written_middle_c.setter
#    def sounding_pitch_of_written_middle_c(self, pitch):
#        return Instrument.sounding_pitch_of_written_middle_c.fset(
#            self, pitch)
