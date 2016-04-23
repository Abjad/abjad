# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoSaxophone(Instrument):
    r'''An alto saxophone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> alto_saxophone = instrumenttools.AltoSaxophone()
        >>> attach(alto_saxophone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "Alto saxophone" }
            \set Staff.shortInstrumentName = \markup { "Alt. sax." }
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
        instrument_name='alto saxophone',
        short_instrument_name='alt. sax.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[Db3, A5]',
        sounding_pitch_of_written_middle_c='Eb3',
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
        self._is_primary_instrument = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto sax.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> alto_sax = instrumenttools.AltoSaxophone()
                >>> print(format(alto_sax))
                instrumenttools.AltoSaxophone(
                    instrument_name='alto saxophone',
                    short_instrument_name='alt. sax.',
                    instrument_name_markup=markuptools.Markup(
                        contents=('Alto saxophone',),
                        ),
                    short_instrument_name_markup=markuptools.Markup(
                        contents=('Alt. sax.',),
                        ),
                    allowable_clefs=indicatortools.ClefInventory(
                        [
                            indicatortools.Clef(
                                name='treble',
                                ),
                            ]
                        ),
                    pitch_range=pitchtools.PitchRange(
                        range_string='[Db3, A5]',
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('ef'),
                    )

        Returns string.
        '''
        superclass = super(AltoSaxophone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto saxophone's allowable clefs.

        ..  container:: example

            ::

                >>> alto_saxophone.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(alto_saxophone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets alto saxophone's name.

        ..  container:: example

            ::

                >>> alto_saxophone.instrument_name
                'alto saxophone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets alto saxophone's instrument name markup.

        ..  container:: example

            ::

                >>> alto_saxophone.instrument_name_markup
                Markup(contents=('Alto saxophone',))

            ::

                >>> show(alto_saxophone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto saxophone's range.

        ..  container:: example

            ::

                >>> alto_saxophone.pitch_range
                PitchRange(range_string='[Db3, A5]')

            ::

                >>> show(alto_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets alto saxophone's short instrument name.

        ..  container:: example

            ::

                >>> alto_saxophone.short_instrument_name
                'alt. sax.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets alto saxophone's short instrument name markup.

        ..  container:: example

            ::

                >>> alto_saxophone.short_instrument_name_markup
                Markup(contents=('Alt. sax.',))

            ::

                >>> show(alto_saxophone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of alto saxophone's written middle C.

        ..  container:: example

            ::

                >>> alto_saxophone.sounding_pitch_of_written_middle_c
                NamedPitch('ef')

            ::

                >>> show(alto_saxophone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
