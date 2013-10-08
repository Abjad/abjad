# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Flute import Flute


class AltoFlute(Flute):
    r'''An alto flute.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> alto_flute = instrumenttools.AltoFlute()
        >>> alto_flute = alto_flute.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto flute }
            \set Staff.shortInstrumentName = \markup { Alt. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The alto flute targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Flute.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('g')
        self._default_instrument_name = 'alto flute'
        self._default_pitch_range = pitchtools.PitchRange(-5, 31)
        self._default_short_instrument_name = 'alt. fl.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._is_primary_instrument = False

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> alto_flute.sounding_pitch_of_written_middle_c
                NamedPitch('g')

            ::

                >>> alto_flute.sounding_pitch_of_written_middle_c = 'gs'
                >>> alto_flute.sounding_pitch_of_written_middle_c
                NamedPitch('gs')

            ::

                >>> alto_flute.sounding_pitch_of_written_middle_c = None
                >>> alto_flute.sounding_pitch_of_written_middle_c
                NamedPitch('g')

            Returns named pitch.
            '''
            return Flute.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            return Flute.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
