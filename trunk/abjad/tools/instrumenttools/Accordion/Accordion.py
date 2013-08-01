# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.KeyboardInstrument import KeyboardInstrument
from abjad.tools.instrumenttools.ReedInstrument import ReedInstrument


class Accordion(KeyboardInstrument, ReedInstrument):
    r'''Abjad model of the accordion:

    ::

        >>> piano_staff = scoretools.PianoStaff(
        ...     [Staff("c'8 d'8 e'8 f'8"), Staff("c'4 b4")])

    ::

        >>> accordion = instrumenttools.Accordion()
        >>> accordion
        Accordion()

    ::

        >>> accordion.attach(piano_staff)
        Accordion()(PianoStaff<<2>>)

    ::

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

    ::

        >>> show(piano_staff) # doctest: +SKIP

    The accordion targets piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    _default_instrument_name = 'accordion'

    #_default_performer_names.append('accordionist')

    _default_short_instrument_name = 'acc.'

    _is_primary_instrument = True

    _primary_clefs = [
        contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]

    _traditional_pitch_range = (-32, 48)

    ### INITIALIZER ###

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        KeyboardInstrument.__init__(
            self, target_context=target_context, **kwargs)
        self._default_instrument_name = 'accordion'
        self._default_performer_names.append('accordionist')
        self._default_short_instrument_name = 'acc.'
        self._is_primary_instrument = True
        self.primary_clefs = [
            contexttools.ClefMark('treble'), contexttools.ClefMark('bass')]
        self._copy_primary_clefs_to_all_clefs()
        self._traditional_pitch_range = pitchtools.PitchRange(-32, 48)

    ### PRIVATE PROPERTIES ###

    # TODO: extend class definition to allow for custom target context in repr
    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return ()

    ### PUBLIC PROPERTIES ###

    @property
    def default_instrument_name(self):
        r'''Default instrument name:

        ::

            >>> accordion.default_instrument_name
            'accordion'

        Return string.
        '''
        return self._default_instrument_name

    @property
    def default_performer_names(self):
        r'''Default instrument name:

        ::

            >>> for name in accordion.default_performer_names:
            ...     name
            'instrumentalist'
            'keyboardist'
            'accordionist'

        Return list.
        '''
        return self._default_performer_names

    @property
    def default_pitch_range(self):
        r'''Primary clefs:

        ::

            >>> accordion.default_pitch_range
            PitchRange('[E1, C8]')

        Return pitch range.
        '''
        return self._traditional_pitch_range

    @property
    def default_short_instrument_name(self):
        r'''Default short instrument name:

        ::

            >>> accordion.default_short_instrument_name
            'acc.'

        Return string.
        '''
        return self._default_short_instrument_name

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

#    @property
#    def primary_clefs(self):
#        r'''Primary clefs:
#
#        ::
#
#            >>> for clef in accordion.primary_clefs:
#            ...     clef
#
#        Return list.
#        '''
#        return self._primary_clefs
