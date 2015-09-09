# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassVoice(Instrument):
    r'''A bass.

    ::

        >>> staff = Staff("c4 d4 e4 fs4")
        >>> bass = instrumenttools.BassVoice()
        >>> attach(bass, staff)
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Bass }
            \set Staff.shortInstrumentName = \markup { Bass }
            c4
            d4
            e4
            fs4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bass',
        short_instrument_name='bass',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[E2, F4]',
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
            'bass',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass's allowable clefs.

        ..  container:: example

            ::

                >>> bass.allowable_clefs
                ClefInventory([Clef(name='bass')])

            ::

                >>> show(bass.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets bass's name.

        ..  container:: example

            ::

                >>> bass.instrument_name
                'bass'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets bass's instrument name markup.

        ..  container:: example

            ::

                >>> bass.instrument_name_markup
                Markup(contents=('Bass',))

            ::

                >>> show(bass.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass's range.

        ..  container:: example

            ::

                >>> bass.pitch_range
                PitchRange(range_string='[E2, F4]')

            ::

                >>> show(bass.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets bass's short instrument name.

        ..  container:: example

            ::

                >>> bass.short_instrument_name
                'bass'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets bass's short instrument name markup.

        ..  container:: example

            ::

                >>> bass.short_instrument_name_markup
                Markup(contents=('Bass',))

            ::

                >>> show(bass.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of bass's written middle C.

        ..  container:: example

            ::

                >>> bass.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(bass.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
