# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class FrenchHorn(Instrument):
    r'''A French horn.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> french_horn = instrumenttools.FrenchHorn()
        >>> attach(french_horn, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Horn }
            \set Staff.shortInstrumentName = \markup { Hn. }
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
        instrument_name='horn',
        short_instrument_name='hn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'treble'),
        pitch_range='[B1, F5]',
        sounding_pitch_of_written_middle_c='F3',
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
            'brass player',
            'hornist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['bass'])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets French horn's allowable clefs.

        ..  container:: example

            ::

                >>> french_horn.allowable_clefs
                ClefInventory([Clef(name='bass'), Clef(name='treble')])

            ::

                >>> show(french_horn.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets French horn's name.

        ..  container:: example

            ::

                >>> french_horn.instrument_name
                'horn'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets French horn's instrument name markup.

        ..  container:: example

            ::

                >>> french_horn.instrument_name_markup
                Markup(contents=('Horn',))

            ::

                >>> show(french_horn.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets French horn's range.

        ..  container:: example

            ::

                >>> french_horn.pitch_range
                PitchRange(range_string='[B1, F5]')

            ::

                >>> show(french_horn.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets French horn's short instrument name.

        ..  container:: example

            ::

                >>> french_horn.short_instrument_name
                'hn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets French horn's short instrument name markup.

        ..  container:: example

            ::

                >>> french_horn.short_instrument_name_markup
                Markup(contents=('Hn.',))

            ::

                >>> show(french_horn.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of French horn's written middle C.

        ..  container:: example

            ::

                >>> french_horn.sounding_pitch_of_written_middle_c
                NamedPitch('f')

            ::

                >>> show(french_horn.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
