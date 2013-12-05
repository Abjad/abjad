# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassFlute(Instrument):
    r'''A contrabass flute.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> contrabass_flute = instrumenttools.ContrabassFlute()
        >>> attach(contrabass_flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Contrabass flute }
            \set Staff.shortInstrumentName = \markup { Cbass. fl. }
            c'8
            d'8
            e'8
            f'8
        }

    The contrabass flute targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='contrabass flute',
        short_instrument_name='cbass. fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='g,',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-17, 19)
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
        self._performer_names.extend([
            'wind player',
            'flautist',
            'flutist',
            ])
