# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Oboe(Instrument):
    r'''An oboe.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> oboe = instrumenttools.Oboe()
        >>> attach(oboe, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Oboe }
            \set Staff.shortInstrumentName = \markup { Ob. }
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
        instrument_name='oboe',
        short_instrument_name='ob.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[Bb3, A6]',
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
            'reed player',
            'double reed player',
            'oboist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets oboe's allowable clefs.

        ..  container:: example

            ::

                >>> oboe.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(oboe.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets oboe's name.

        ..  container:: example

            ::

                >>> oboe.instrument_name
                'oboe'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets oboe's instrument name markup.

        ..  container:: example

            ::

                >>> oboe.instrument_name_markup
                Markup(contents=('Oboe',))

            ::

                >>> show(oboe.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets oboe's range.

        ..  container:: example

            ::

                >>> oboe.pitch_range
                PitchRange(range_string='[Bb3, A6]')

            ::

                >>> show(oboe.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets oboe's short instrument name.

        ..  container:: example

            ::

                >>> oboe.short_instrument_name
                'ob.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets oboe's short instrument name markup.

        ..  container:: example

            ::

                >>> oboe.short_instrument_name_markup
                Markup(contents=('Ob.',))

            ::

                >>> show(oboe.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of oboe's written middle C.

        ..  container:: example

            ::

                >>> oboe.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(oboe.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
