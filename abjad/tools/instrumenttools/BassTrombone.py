# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassTrombone(Instrument):
    r'''Bass trombone.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> bass_trombone = abjad.instrumenttools.BassTrombone()
            >>> abjad.attach(bass_trombone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Bass trombone" }
                \set Staff.shortInstrumentName = \markup { "Bass trb." }
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
        instrument_name='bass trombone',
        short_instrument_name='bass trb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[C2, F4]',
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
            'brass player',
            'trombonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass trombone's allowable clefs.

        ..  container:: example

            ::

                >>> bass_trombone.allowable_clefs
                ClefList([Clef(name='bass')])

            ::

                >>> show(bass_trombone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets bass trombone's name.

        ..  container:: example

            ::

                >>> bass_trombone.instrument_name
                'bass trombone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets bass trombone's instrument name markup.

        ..  container:: example

            ::

                >>> bass_trombone.instrument_name_markup
                Markup(contents=['Bass trombone'])

            ::

                >>> show(bass_trombone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass trombone's range.

        ..  container:: example

            ::

                >>> bass_trombone.pitch_range
                PitchRange('[C2, F4]')

            ::

                >>> show(bass_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets bass trombone's short instrument name.

        ..  container:: example

            ::

                >>> bass_trombone.short_instrument_name
                'bass trb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets bass trombone's short instrument name markup.

        ..  container:: example

            ::

                >>> bass_trombone.short_instrument_name_markup
                Markup(contents=['Bass trb.'])

            ::

                >>> show(bass_trombone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of bass_trombone's written middle C.

        ..  container:: example

            ::

                >>> bass_trombone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(bass_trombone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
