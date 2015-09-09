# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Marimba(Instrument):
    r'''A marimba.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> marimba = instrumenttools.Marimba()
        >>> attach(marimba, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Marimba }
            \set Staff.shortInstrumentName = \markup { Mb. }
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
        instrument_name='marimba',
        short_instrument_name='mb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[F2, C7]',
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
            'percussionist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets marimba's allowable clefs.

        ..  container:: example

            ::

                >>> marimba.allowable_clefs
                ClefInventory([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(marimba.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets marimba's name.

        ..  container:: example

            ::

                >>> marimba.instrument_name
                'marimba'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets marimba's instrument name markup.

        ..  container:: example

            ::

                >>> marimba.instrument_name_markup
                Markup(contents=('Marimba',))

            ::

                >>> show(marimba.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets marimba's range.

        ..  container:: example

            ::

                >>> marimba.pitch_range
                PitchRange(range_string='[F2, C7]')

            ::

                >>> show(marimba.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets marimba's short instrument name.

        ..  container:: example

            ::

                >>> marimba.short_instrument_name
                'mb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets marimba's short instrument name markup.

        ..  container:: example

            ::

                >>> marimba.short_instrument_name_markup
                Markup(contents=('Mb.',))

            ::

                >>> show(marimba.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of marimba's written middle C.

        ..  container:: example

            ::

                >>> marimba.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(marimba.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
