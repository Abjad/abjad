# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class EnglishHorn(Instrument):
    r'''A English horn.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> english_horn = instrumenttools.EnglishHorn()
        >>> attach(english_horn, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { English horn }
            \set Staff.shortInstrumentName = \markup { Eng. hn. }
            c'8
            d'8
            e'8
            f'8
        }

    The English horn targets staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='English horn',
        short_instrument_name='Eng. hn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='f',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-8, 24)
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
            'reed player',
            'double reed player',
            'oboist',
            ])
