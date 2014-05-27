# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Trumpet(Instrument):
    r'''A trumpet.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> trumpet = instrumenttools.Trumpet()
        >>> attach(trumpet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Trumpet }
            \set Staff.shortInstrumentName = \markup { Tp. }
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
        instrument_name='trumpet',
        short_instrument_name='tp.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[F#3, D6]',
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
            'trumpeter',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets trumpet's allowable clefs.

        ..  container:: example

            ::

                >>> trumpet.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(trumpet.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets trumpet's name.

        ..  container:: example

            ::

                >>> trumpet.instrument_name
                'trumpet'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets trumpet's instrument name markup.

        ..  container:: example

            ::

                >>> trumpet.instrument_name_markup
                Markup(contents=('Trumpet',))

            ::

                >>> show(trumpet.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets trumpet's range.

        ..  container:: example

            ::

                >>> trumpet.pitch_range
                PitchRange(range_string='[F#3, D6]')

            ::

                >>> show(trumpet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets trumpet's short instrument name.

        ..  container:: example

            ::

                >>> trumpet.short_instrument_name
                'tp.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets trumpet's short instrument name markup.

        ..  container:: example

            ::

                >>> trumpet.short_instrument_name_markup
                Markup(contents=('Tp.',))

            ::

                >>> show(trumpet.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of trumpet's written middle C.

        ..  container:: example

            ::

                >>> trumpet.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(trumpet.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
