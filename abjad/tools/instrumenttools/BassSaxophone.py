# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassSaxophone(Instrument):
    r'''A bass saxophone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> bass_saxophone = instrumenttools.BassSaxophone()
        >>> attach(bass_saxophone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "Bass saxophone" }
            \set Staff.shortInstrumentName = \markup { "Bass sax." }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='bass saxophone',
        short_instrument_name='bass sax.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[Ab2, E4]',
        sounding_pitch_of_written_middle_c='Bb1',
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
            'single reed player',
            'saxophonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass saxophone's allowable clefs.

        ..  container:: example

            ::

                >>> bass_saxophone.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(bass_saxophone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets bass saxophone's name.

        ..  container:: example

            ::

                >>> bass_saxophone.instrument_name
                'bass saxophone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets bass saxophone's instrument name markup.

        ..  container:: example

            ::

                >>> bass_saxophone.instrument_name_markup
                Markup(contents=('Bass saxophone',))

            ::

                >>> show(bass_saxophone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass saxophone's range.

        ..  container:: example

            ::

                >>> bass_saxophone.pitch_range
                PitchRange(range_string='[Ab2, E4]')

            ::

                >>> show(bass_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets bass saxophone's short instrument name.

        ..  container:: example

            ::

                >>> bass_saxophone.short_instrument_name
                'bass sax.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets bass saxophone's short instrument name markup.

        ..  container:: example

            ::

                >>> bass_saxophone.short_instrument_name_markup
                Markup(contents=('Bass sax.',))

            ::

                >>> show(bass_saxophone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of bass_saxophone's written middle C.

        ..  container:: example

            ::

                >>> bass_saxophone.sounding_pitch_of_written_middle_c
                NamedPitch('bf,,')

            ::

                >>> show(bass_saxophone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
