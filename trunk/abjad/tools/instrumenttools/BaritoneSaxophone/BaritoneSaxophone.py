# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Saxophone.Saxophone import Saxophone


class BaritoneSaxophone(Saxophone):
    r'''A baritone saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> baritone_sax = instrumenttools.BaritoneSaxophone()
        >>> baritone_sax = baritone_sax.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone saxophone }
            \set Staff.shortInstrumentName = \markup { Bar. sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The baritone saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Saxophone.__init__(self, **kwargs)
        self._default_instrument_name = 'baritone saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'bar. sax.'
        self._is_primary_instrument = False
        pitch = pitchtools.NamedPitch('ef,')
        self._default_sounding_pitch_of_written_middle_c = pitch
        self.starting_clefs = [contexttools.ClefMark('treble')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-24, 8)

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> baritone_sax.sounding_pitch_of_written_middle_c
                NamedPitch('ef,')

            ::

                >>> baritone_sax.sounding_pitch_of_written_middle_c = 'e' 
                >>> baritone_sax.sounding_pitch_of_written_middle_c
                NamedPitch('e')

            ::

                >>> baritone_sax.sounding_pitch_of_written_middle_c = None
                >>> baritone_sax.sounding_pitch_of_written_middle_c
                NamedPitch('ef,')

            Returns named pitch.
            '''
            return Saxophone.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Saxophone.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
