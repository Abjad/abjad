# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Bassoon(Instrument):
    r'''Bassoon.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> bassoon = abjad.instrumenttools.Bassoon()
            >>> abjad.attach(bassoon, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Bassoon }
                \set Staff.shortInstrumentName = \markup { Bsn. }
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bassoon',
        short_instrument_name='bsn.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'tenor'),
        pitch_range='[Bb1, Eb5]',
        middle_c_sounding_pitch=None,
        ):
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            middle_c_sounding_pitch=\
                middle_c_sounding_pitch,
            )
        self._performer_names.extend([
            'wind player',
            'reed player',
            'double reed player',
            'bassoonist',
            ])
        self._starting_clefs = type(self.allowable_clefs)(['bass'])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bassoon's allowable clefs.

        ..  container:: example

            ::

                >>> bassoon.allowable_clefs
                ClefList([Clef(name='bass'), Clef(name='tenor')])

            ::

                >>> show(bassoon.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets bassoon's name.

        ..  container:: example

            ::

                >>> bassoon.instrument_name
                'bassoon'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets bassoon's instrument name markup.

        ..  container:: example

            ::

                >>> bassoon.instrument_name_markup
                Markup(contents=['Bassoon'])

            ::

                >>> show(bassoon.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bassoon's range.

        ..  container:: example

            ::

                >>> bassoon.pitch_range
                PitchRange('[Bb1, Eb5]')

            ::

                >>> show(bassoon.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets bassoon's short instrument name.

        ..  container:: example

            ::

                >>> bassoon.short_instrument_name
                'bsn.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets bassoon's short instrument name markup.

        ..  container:: example

            ::

                >>> bassoon.short_instrument_name_markup
                Markup(contents=['Bsn.'])

            ::

                >>> show(bassoon.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bassoon's written middle C.

        ..  container:: example

            ::

                >>> bassoon.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(bassoon.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)
