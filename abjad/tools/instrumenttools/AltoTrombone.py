# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoTrombone(Instrument):
    r'''An alto trombone.

    ::

        >>> staff = Staff("c4 d4 e4 fs4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> alto_trombone = instrumenttools.AltoTrombone()
        >>> attach(alto_trombone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { "Alto trombone" }
            \set Staff.shortInstrumentName = \markup { "Alt. trb." }
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
        instrument_name='alto trombone',
        short_instrument_name='alt. trb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'tenor'),
        pitch_range='[A2, Bb5]',
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
        self._starting_clefs = indicatortools.ClefInventory(['bass'])

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto trombone.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> alto_trombone = instrumenttools.AltoTrombone()
                >>> print(format(alto_trombone))
                instrumenttools.AltoTrombone(
                    instrument_name='alto trombone',
                    short_instrument_name='alt. trb.',
                    instrument_name_markup=markuptools.Markup(
                        contents=('Alto trombone',),
                        ),
                    short_instrument_name_markup=markuptools.Markup(
                        contents=('Alt. trb.',),
                        ),
                    allowable_clefs=indicatortools.ClefInventory(
                        [
                            indicatortools.Clef(
                                name='bass',
                                ),
                            indicatortools.Clef(
                                name='tenor',
                                ),
                            ]
                        ),
                    pitch_range=pitchtools.PitchRange(
                        range_string='[A2, Bb5]',
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                    )

        Returns string.
        '''
        superclass = super(AltoTrombone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto trombone's allowable clefs.

        ..  container:: example

            ::

                >>> alto_trombone.allowable_clefs
                ClefInventory([Clef(name='bass'), Clef(name='tenor')])

            ::

                >>> show(alto_trombone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets alto trombone's name.

        ..  container:: example

            ::

                >>> alto_trombone.instrument_name
                'alto trombone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets alto trombone's instrument name markup.

        ..  container:: example

            ::

                >>> alto_trombone.instrument_name_markup
                Markup(contents=('Alto trombone',))

            ::

                >>> show(alto_trombone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto trombone's range.

        ..  container:: example

            ::

                >>> alto_trombone.pitch_range
                PitchRange(range_string='[A2, Bb5]')

            ::

                >>> show(alto_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets alto trombone's short instrument name.

        ..  container:: example

            ::

                >>> alto_trombone.short_instrument_name
                'alt. trb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets alto trombone's short instrument name markup.

        ..  container:: example

            ::

                >>> alto_trombone.short_instrument_name_markup
                Markup(contents=('Alt. trb.',))

            ::

                >>> show(alto_trombone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of alto trombone's written middle C.

        ..  container:: example

            ::

                >>> alto_trombone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(alto_trombone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
