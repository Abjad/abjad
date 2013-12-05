# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BaritoneVoice(Instrument):
    r'''A baritone voice.

    ::

        >>> staff = Staff("c8 d8 e8 f8")
        >>> show(staff) # doctest: +SKIP
        >>> baritone_voice = instrumenttools.BaritoneVoice()
        >>> attach(baritone_voice, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone }
            \set Staff.shortInstrumentName = \markup { Bar. }
            c8
            d8
            e8
            f8
        }

    The baritone voice targets staff context by default.
    '''
    
    ### CLASS VARIABLES ###

    __slots__ = ()
    
    # TODO: what is this? Shouldn't this be removed?
    default_performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='baritone',
        short_instrument_name='bar.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        allowable_clefs = allowable_clefs or indicatortools.ClefInventory(
            ['bass'])
        pitch_range = pitch_range or pitchtools.PitchRange('[A2, A4]')
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
        self._performer_names.extend([
            'vocalist',
            'baritone',
            ])
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
        self._is_primary_instrument = True

#    ### PUBLIC PROPERTIES ###
#
#    @property
#    def sounding_pitch_of_written_middle_c(self):
#        r'''Gets and sets sounding pitch of written middle C.
#
#        ::
#
#            >>> baritone_voice.sounding_pitch_of_written_middle_c
#            NamedPitch("c'")
#
#        ::
#
#            >>> baritone_voice.sounding_pitch_of_written_middle_c = 'g'
#            >>> baritone_voice.sounding_pitch_of_written_middle_c
#            NamedPitch('g')
#
#        Returns named pitch.
#        '''
#        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
#
#    @sounding_pitch_of_written_middle_c.setter
#    def sounding_pitch_of_written_middle_c(self, pitch):
#        Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
