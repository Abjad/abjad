# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Vibraphone(Instrument):
    r'''A vibraphone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> vibraphone = instrumenttools.Vibraphone()
        >>> attach(vibraphone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Vibraphone }
            \set Staff.shortInstrumentName = \markup { Vibr. }
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
        instrument_name='vibraphone',
        short_instrument_name='vibr.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[F3, F6]',
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
            'vibraphonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets vibraphone's allowable clefs.

        ..  container:: example

            ::

                >>> vibraphone.allowable_clefs
                ClefInventory([Clef('treble')])

            ::

                >>> show(vibraphone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets vibraphone's name.

        ..  container:: example

            ::

                >>> vibraphone.instrument_name
                'vibraphone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets vibraphone's instrument name markup.

        ..  container:: example

            ::

                >>> vibraphone.instrument_name_markup
                Markup(('Vibraphone',))

            ::

                >>> show(vibraphone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets vibraphone's range.

        ..  container:: example

            ::

                >>> vibraphone.pitch_range
                PitchRange('[F3, F6]')

            ::

                >>> show(vibraphone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets vibraphone's short instrument name.

        ..  container:: example

            ::

                >>> vibraphone.short_instrument_name
                'vibr.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets vibraphone's short instrument name markup.

        ..  container:: example

            ::

                >>> vibraphone.short_instrument_name_markup
                Markup(('Vibr.',))

            ::

                >>> show(vibraphone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of vibraphone's written middle C.

        ..  container:: example

            ::

                >>> vibraphone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(vibraphone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
