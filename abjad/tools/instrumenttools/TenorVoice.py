# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorVoice(Instrument):
    r'''A tenor voice.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> tenor = instrumenttools.TenorVoice()
        >>> attach(tenor, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Tenor }
            \set Staff.shortInstrumentName = \markup { Ten. }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'ten.'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='tenor',
        short_instrument_name='ten.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[C3, D5]',
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
            'vocalist',
            'tenor',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tenor's allowable clefs.

        ..  container:: example

            ::

                >>> tenor.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(tenor.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets tenor's name.

        ..  container:: example

            ::

                >>> tenor.instrument_name
                'tenor'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets tenor's instrument name markup.

        ..  container:: example

            ::

                >>> tenor.instrument_name_markup
                Markup(contents=('Tenor',))

            ::

                >>> show(tenor.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor's range.

        ..  container:: example

            ::

                >>> tenor.pitch_range
                PitchRange(range_string='[C3, D5]')

            ::

                >>> show(tenor.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets tenor's short instrument name.

        ..  container:: example

            ::

                >>> tenor.short_instrument_name
                'ten.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets tenor's short instrument name markup.

        ..  container:: example

            ::

                >>> tenor.short_instrument_name_markup
                Markup(contents=('Ten.',))

            ::

                >>> show(tenor.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of tenor's written middle C.

        ..  container:: example

            ::

                >>> tenor.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(tenor.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
