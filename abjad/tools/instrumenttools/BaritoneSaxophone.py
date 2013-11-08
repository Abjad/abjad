# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BaritoneSaxophone(Instrument):
    r'''A baritone saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP
        >>> baritone_sax = instrumenttools.BaritoneSaxophone()
        >>> baritone_sax = attach(baritone_sax, staff)
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
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('ef,')
        self._default_instrument_name = 'baritone saxophone'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._default_short_instrument_name = 'bar. sax.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = marktools.ClefMarkInventory([
            marktools.Clef('treble'),
            ])
        self._default_pitch_range = pitchtools.PitchRange(-24, 8)
        self._is_primary_instrument = False
        self._copy_default_starting_clefs_to_default_allowable_clefs()

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
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
