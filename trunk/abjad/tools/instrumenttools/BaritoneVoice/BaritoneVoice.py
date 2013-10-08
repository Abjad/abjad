# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Voice import Voice


class BaritoneVoice(Voice):
    r'''A baritone voice.

    ::

        >>> staff = Staff("c8 d8 e8 f8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> baritone_voice = instrumenttools.BaritoneVoice()
        >>> baritone_voice = baritone_voice.attach(staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Baritone voice }
            \set Staff.shortInstrumentName = \markup { Baritone }
            c8
            d8
            e8
            f8
        }

    The baritone voice targets staff context by default.
    '''
    
    ### CLASS VARIABLES ###

    # TODO: what is this? Shouldn't this be removed?
    default_performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Voice.__init__(self, **kwargs)
        self._default_instrument_name = 'baritone voice'
        self._default_performer_names.append('baritone')
        self._default_short_instrument_name = 'baritone'
        self._is_primary_instrument = True
        self.starting_clefs = [contexttools.ClefMark('bass')]
        self._copy_starting_clefs_to_allowable_clefs()
        self._default_pitch_range = pitchtools.PitchRange(('A2', 'A4'))

    ### PUBLIC PROPERTIES ###

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ::

                >>> baritone_voice.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> baritone_voice.sounding_pitch_of_written_middle_c = 'g'
                >>> baritone_voice.sounding_pitch_of_written_middle_c
                NamedPitch('g')

            Returns named pitch.
            '''
            return Voice.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, foo):
            Voice.sounding_pitch_of_written_middle_c.fset(self, foo)
        return property(**locals())
