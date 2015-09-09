# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Flute(Instrument):
    r'''A flute.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> flute = instrumenttools.Flute()
        >>> attach(flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Flute }
            \set Staff.shortInstrumentName = \markup { Fl. }
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
        instrument_name='flute',
        short_instrument_name='fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[C4, D7]',
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
            'wind player',
            'flautist',
            'flutist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets flute's allowable clefs.

        ..  container:: example

            ::

                >>> flute.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(flute.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets flute's name.

        ..  container:: example

            ::

                >>> flute.instrument_name
                'flute'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets flute's instrument name markup.

        ..  container:: example

            ::

                >>> flute.instrument_name_markup
                Markup(contents=('Flute',))

            ::

                >>> show(flute.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets flute's range.

        ..  container:: example

            ::

                >>> flute.pitch_range
                PitchRange(range_string='[C4, D7]')

            ::

                >>> show(flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets flute's short instrument name.

        ..  container:: example

            ::

                >>> flute.short_instrument_name
                'fl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets flute's short instrument name markup.

        ..  container:: example

            ::

                >>> flute.short_instrument_name_markup
                Markup(contents=('Fl.',))

            ::

                >>> show(flute.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of flute's written middle C.

        ..  container:: example

            ::

                >>> flute.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(flute.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
