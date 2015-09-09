# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Tuba(Instrument):
    r'''A tuba.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> tuba = instrumenttools.Tuba()
        >>> attach(tuba, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tuba }
            \set Staff.shortInstrumentName = \markup { Tb. }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='tuba',
        short_instrument_name='tb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[D1, F4]',
        sounding_pitch_of_written_middle_c=None,
        ):
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
            'brass player',
            'tubist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tuba's allowable clefs.

        ..  container:: example

            ::

                >>> tuba.allowable_clefs
                ClefInventory([Clef(name='bass')])

            ::

                >>> show(tuba.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets tuba's name.

        ..  container:: example

            ::

                >>> tuba.instrument_name
                'tuba'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets tuba's instrument name markup.

        ..  container:: example

            ::

                >>> tuba.instrument_name_markup
                Markup(contents=('Tuba',))

            ::

                >>> show(tuba.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tuba's range.

        ..  container:: example

            ::

                >>> tuba.pitch_range
                PitchRange(range_string='[D1, F4]')

            ::

                >>> show(tuba.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets tuba's short instrument name.

        ..  container:: example

            ::

                >>> tuba.short_instrument_name
                'tb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets tuba's short instrument name markup.

        ..  container:: example

            ::

                >>> tuba.short_instrument_name_markup
                Markup(contents=('Tb.',))

            ::

                >>> show(tuba.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of tuba's written middle C.

        ..  container:: example

            ::

                >>> tuba.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(tuba.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
