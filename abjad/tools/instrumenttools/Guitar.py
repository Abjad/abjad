# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools.instrumenttools.Instrument import Instrument


class Guitar(Instrument):
    r'''A guitar.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> guitar = instrumenttools.Guitar()
        >>> attach(guitar, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Guitar }
            \set Staff.shortInstrumentName = \markup { Gt. }
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
        instrument_name='guitar',
        short_instrument_name='gt.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        default_tuning=('E2', 'A2', 'D3', 'G3', 'B3', 'E4'),
        pitch_range='[E2, E5]',
        sounding_pitch_of_written_middle_c='C3',
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
            'guitarist',
            ])
        self._is_primary_instrument = True
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets guitar's allowable clefs.

        ..  container:: example

            ::

                >>> guitar.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(guitar.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets guitar's default tuning.

        ..  container:: example

            ::

                >>> guitar.default_tuning
                Tuning(pitches=PitchSegment(['e,', 'a,', 'd', 'g', 'b', "e'"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def instrument_name(self):
        r'''Gets guitar's name.

        ..  container:: example

            ::

                >>> guitar.instrument_name
                'guitar'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets guitar's instrument name markup.

        ..  container:: example

            ::

                >>> guitar.instrument_name_markup
                Markup(contents=('Guitar',))

            ::

                >>> show(guitar.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets guitar's range.

        ..  container:: example

            ::

                >>> guitar.pitch_range
                PitchRange(range_string='[E2, E5]')

            ::

                >>> show(guitar.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets guitar's short instrument name.

        ..  container:: example

            ::

                >>> guitar.short_instrument_name
                'gt.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets guitar's short instrument name markup.

        ..  container:: example

            ::

                >>> guitar.short_instrument_name_markup
                Markup(contents=('Gt.',))

            ::

                >>> show(guitar.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of guitar's written middle C.

        ..  container:: example

            ::

                >>> guitar.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            ::

                >>> show(guitar.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
