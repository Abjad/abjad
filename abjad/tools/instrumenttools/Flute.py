# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Flute(Instrument):
    r'''Flute.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> flute = abjad.instrumenttools.Flute()
            >>> abjad.attach(flute, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Flute }
                \set Staff.shortInstrumentName = \markup { Fl. }
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
        instrument_name='flute',
        short_instrument_name='fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[C4, D7]',
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
            'flautist',
            'flutist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets flute's allowable clefs.

        ..  container:: example

            ::

                >>> flute.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(flute.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets flute's name.

        ..  container:: example

            ::

                >>> flute.instrument_name
                'flute'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets flute's instrument name markup.

        ..  container:: example

            ::

                >>> flute.instrument_name_markup
                Markup(contents=['Flute'])

            ::

                >>> show(flute.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets flute's range.

        ..  container:: example

            ::

                >>> flute.pitch_range
                PitchRange('[C4, D7]')

            ::

                >>> show(flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets flute's short instrument name.

        ..  container:: example

            ::

                >>> flute.short_instrument_name
                'fl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets flute's short instrument name markup.

        ..  container:: example

            ::

                >>> flute.short_instrument_name_markup
                Markup(contents=['Fl.'])

            ::

                >>> show(flute.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of flute's written middle C.

        ..  container:: example

            ::

                >>> flute.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(flute.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)
