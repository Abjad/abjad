# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BaritoneVoice(Instrument):
    r'''A baritone voice.

    ::

        >>> staff = Staff("c4 d4 e4 fs4")
        >>> baritone = instrumenttools.BaritoneVoice()
        >>> attach(baritone, staff)
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Baritone }
            \set Staff.shortInstrumentName = \markup { Bar. }
            c4
            d4
            e4
            fs4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='baritone',
        short_instrument_name='bar.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[A2, A4]',
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
            'baritone',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets baritone's allowable clefs.

        ..  container:: example

            ::

                >>> baritone.allowable_clefs
                ClefInventory([Clef(name='bass')])

            ::

                >>> show(baritone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets baritone's name.

        ..  container:: example

            ::

                >>> baritone.instrument_name
                'baritone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets baritone's instrument name markup.

        ..  container:: example

            ::

                >>> baritone.instrument_name_markup
                Markup(contents=('Baritone',))

            ::

                >>> show(baritone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets baritone's range.

        ..  container:: example

            ::

                >>> baritone.pitch_range
                PitchRange(range_string='[A2, A4]')

            ::

                >>> show(baritone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets baritone's short instrument name.

        ..  container:: example

            ::

                >>> baritone.short_instrument_name
                'bar.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets baritone's short instrument name markup.

        ..  container:: example

            ::

                >>> baritone.short_instrument_name_markup
                Markup(contents=('Bar.',))

            ::

                >>> show(baritone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of baritone's written middle C.

        ..  container:: example

            ::

                >>> baritone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(baritone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
