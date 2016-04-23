# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class EnglishHorn(Instrument):
    r'''A English horn.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> english_horn = instrumenttools.EnglishHorn()
        >>> attach(english_horn, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "English horn" }
            \set Staff.shortInstrumentName = \markup { "Eng. hn." }
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
        instrument_name='English horn',
        short_instrument_name='Eng. hn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[E3, C6]',
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
            'reed player',
            'double reed player',
            'oboist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets English horn's allowable clefs.

        ..  container:: example

            ::

                >>> english_horn.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(english_horn.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets English horn's name.

        ..  container:: example

            ::

                >>> english_horn.instrument_name
                'English horn'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets English horn's instrument name markup.

        ..  container:: example

            ::

                >>> english_horn.instrument_name_markup
                Markup(contents=('English horn',))

            ::

                >>> show(english_horn.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets English horn's range.

        ..  container:: example

            ::

                >>> english_horn.pitch_range
                PitchRange(range_string='[E3, C6]')

            ::

                >>> show(english_horn.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets English horn's short instrument name.

        ..  container:: example

            ::

                >>> english_horn.short_instrument_name
                'Eng. hn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets English horn's short instrument name markup.

        ..  container:: example

            ::

                >>> english_horn.short_instrument_name_markup
                Markup(contents=('Eng. hn.',))

            ::

                >>> show(english_horn.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of English horn's written middle C.

        ..  container:: example

            ::

                >>> english_horn.sounding_pitch_of_written_middle_c
                NamedPitch('f')

            ::

                >>> show(english_horn.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
