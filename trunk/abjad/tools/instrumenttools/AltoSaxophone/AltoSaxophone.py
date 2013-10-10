# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoSaxophone(Instrument):
    r'''An alto saxophone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> alto_saxophone = instrumenttools.AltoSaxophone()
        >>> alto_saxophone = alto_saxophone.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto saxophone }
            \set Staff.shortInstrumentName = \markup { Alto sax. }
            c'8
            d'8
            e'8
            f'8
        }

    The alto saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('ef')
        self._default_instrument_name = 'alto saxophone'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-11, 21)
        self._default_short_instrument_name = 'alto sax.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._default_starting_clefs = [contexttools.ClefMark('treble')]
        self._is_primary_instrument = True
        self._copy_default_starting_clefs_to_default_allowable_clefs()
        #self._make_default_name_markups()

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> alto_saxophone.sounding_pitch_of_written_middle_c
                NamedPitch('ef')

            ::

                >>> alto_saxophone.sounding_pitch_of_written_middle_c = 'e'
                >>> alto_saxophone.sounding_pitch_of_written_middle_c
                NamedPitch('e')

            ::

                >>> alto_saxophone.sounding_pitch_of_written_middle_c = None
                >>> alto_saxophone.sounding_pitch_of_written_middle_c
                NamedPitch('ef')

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
