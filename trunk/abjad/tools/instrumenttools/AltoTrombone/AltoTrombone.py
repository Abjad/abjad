# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Trombone.Trombone import Trombone


class AltoTrombone(Trombone):
    r'''An alto trombone.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> clef = contexttools.ClefMark('bass')
        >>> clef = clef.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ::

        >>> alto_trombone = instrumenttools.AltoTrombone()
        >>> alto_trombone = alto_trombone.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Alto trombone }
            \set Staff.shortInstrumentName = \markup { Alt. trb. }
            c'8
            d'8
            e'8
            f'8
        }

    The alto trombone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Trombone.__init__(self, **kwargs)
        self._default_instrument_name = 'alto trombone'
        self._default_short_instrument_name = 'alt. trb.'
        self._is_primary_instrument = False
        self.starting_clefs = [
            contexttools.ClefMark('bass'), 
            contexttools.ClefMark('tenor'),
            ]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange('[A2, Bb5]')

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> alto_trombone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> alto_trombone.sounding_pitch_of_written_middle_c = 'bf'
                >>> alto_trombone.sounding_pitch_of_written_middle_c
                NamedPitch('bf')

            Returns named pitch.
            '''
            return Trombone.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, foo):
            Trombone.sounding_pitch_of_written_middle_c.fset(self, foo)
        return property(**locals())
