# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools.instrumenttools.Instrument import Instrument


class Violin(Instrument):
    r'''A violin.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> violin = instrumenttools.Violin()
        >>> attach(violin, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Violin }
            \set Staff.shortInstrumentName = \markup { Vn. }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='violin',
        short_instrument_name='vn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        default_tuning=('G3', 'D4', 'A4', 'E5'),
        pitch_range='[G3, G7]',
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
            'string player',
            'violinist',
            ])
        self._is_primary_instrument = True
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets violin's allowable clefs.

        ..  container:: example

            ::

                >>> violin.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(violin.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets violin's default tuning.

        ..  container:: example

            >>> violin.default_tuning
            Tuning(pitches=PitchSegment(['g', "d'", "a'", "e''"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def instrument_name(self):
        r'''Gets violin's name.

        ..  container:: example

            ::

                >>> violin.instrument_name
                'violin'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets violin's instrument name markup.

        ..  container:: example

            ::

                >>> violin.instrument_name_markup
                Markup(contents=('Violin',))

            ::

                >>> show(violin.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets violin's range.

        ..  container:: example

            ::

                >>> violin.pitch_range
                PitchRange(range_string='[G3, G7]')

            ::

                >>> show(violin.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets violin's short instrument name.

        ..  container:: example

            ::

                >>> violin.short_instrument_name
                'vn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets violin's short instrument name markup.

        ..  container:: example

            ::

                >>> violin.short_instrument_name_markup
                Markup(contents=('Vn.',))

            ::

                >>> show(violin.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of violin's written middle C.

        ..  container:: example

            ::

                >>> violin.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(violin.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
