# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.KeyboardInstrument import KeyboardInstrument
from abjad.tools.instrumenttools.ReedInstrument import ReedInstrument


class Accordion(KeyboardInstrument, ReedInstrument):
    r'''An accordion.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'8 d'8 e'8 f'8"))
        >>> piano_staff.append(Staff("c'4 b4"))
        >>> show(piano_staff) # doctest: +SKIP

    ::

        >>> accordion = instrumenttools.Accordion()
        >>> accordion = accordion.attach(piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Accordion }
            \set PianoStaff.shortInstrumentName = \markup { Acc. }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                b4
            }
        >>

    The accordion targets the piano staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        KeyboardInstrument.__init__(
            self, 
            target_context=target_context, 
            **kwargs
            )
        self._default_instrument_name = 'accordion'
        self._default_performer_names.append('accordionist')
        self._default_short_instrument_name = 'acc.'
        self._is_primary_instrument = True
        self.primary_clefs = [
            contexttools.ClefMark('treble'), 
            contexttools.ClefMark('bass'),
            ]
        self._copy_primary_clefs_to_all_clefs()
        self._default_pitch_range = pitchtools.PitchRange(-32, 48)

    ### PRIVATE PROPERTIES ###

    # TODO: extend class definition to allow for custom target context in repr
    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return ()

    ### PUBLIC PROPERTIES ###

    @apply
    def instrument_name():
        def fget(self):
            r'''Get instrument name.

            ::

                >>> accordion.instrument_name
                'accordion'

            Returns string.

            Set instrument name:
            
            ::

                >>> accordion.instrument_name = 'fisarmonica'
                >>> accordion.instrument_name
                'fisarmonica'

            Returns none.
            '''
            return KeyboardInstrument.instrument_name.fget(self)
        def fset(self, foo):
            KeyboardInstrument.instrument_name.fset(self, foo)
        return property(**locals())

    @property
    def is_primary_instrument(self):
        r'''True when instrument is primary.
        Otherwise false:

        ::

            >>> accordion.is_primary_instrument
            True

        Return string.
        '''
        return self._is_primary_instrument

    @apply
    def pitch_range():
        def fget(self):
            r'''Gets and sets pitch range.

            ::

                >>> accordion.pitch_range
                PitchRange('[E1, C8]')

            ::

                >>> pitch_range = pitchtools.PitchRange(0, 39)
                >>> accordion.pitch_range = pitch_range

            Returns pitch range.
            '''
            superclass = KeyboardInstrument
            return superclass.pitch_range.fget(self)
        def fset(self, pitch_range):
            superclass = KeyboardInstrument
            superclass.pitch_range.fset(self, pitch_range)
        return property(**locals())

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets sounding pitch of written middle C.

            ::

                >>> accordion.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            Sets sounding pitch of written middle C:

            ::

                >>> accordion.sounding_pitch_of_written_middle_c = 'g'
                >>> accordion.sounding_pitch_of_written_middle_c
                NamedPitch('g')

            Returns named pitch.
            '''
            superclass = KeyboardInstrument
            return superclass.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, foo):
            superclass = KeyboardInstrument
            superclass.sounding_pitch_of_written_middle_c.fset(self, foo)
        return property(**locals())
