# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Harp(Instrument):
    r'''A harp.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'4 d'4 e'4 f'4"))
        >>> piano_staff.append(Staff("c'2 b2"))
        >>> harp = instrumenttools.Harp()
        >>> attach(harp, piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Harp }
            \set PianoStaff.shortInstrumentName = \markup { Hp. }
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                c'2
                b2
            }
        >>

    The harp targets piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='harp',
        short_instrument_name='hp.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        from abjad.tools import scoretools
        allowable_clefs = indicatortools.ClefInventory(['treble', 'bass'])
        pitch_range = pitch_range or pitchtools.PitchRange(-37, 44)
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
        self._default_scope = scoretools.PianoStaff
        self._performer_names.extend([
            'string player',
            'harpist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['treble', 'bass'])
