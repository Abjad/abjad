# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassFlute(Instrument):
    r'''A bass flute.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> bass_flute = instrumenttools.BassFlute()
        >>> bass_flute = bass_flute.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
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

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('c')
        self._default_instrument_name = 'bass flute'
        self._default_performer_names.extend([
            'wind player',
            'flautist',
            'flutist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-12, 24)
        self._default_short_instrument_name = 'bass fl.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._is_primary_instrument = False

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> bass_flute.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            ::

                >>> bass_flute.sounding_pitch_of_written_middle_c = 'cs'
                >>> bass_flute.sounding_pitch_of_written_middle_c
                NamedPitch('cs')

            ::

                >>> bass_flute.sounding_pitch_of_written_middle_c = None
                >>> bass_flute.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            return Instrument.sounding_pitch_of_written_middle_c.fset(
                self, pitch)
        return property(**locals())
