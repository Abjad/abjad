# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoFlute(Instrument):
    r'''Alto flute.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> alto_flute = abjad.instrumenttools.AltoFlute()
            >>> abjad.attach(alto_flute, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Alto flute" }
                \set Staff.shortInstrumentName = \markup { "Alt. fl." }
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
        instrument_name='alto flute',
        short_instrument_name='alt. fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[G3, G6]',
        sounding_pitch_of_written_middle_c='G3',
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
            'flautist',
            'flutist',
            ])
        self._starting_clefs = type(self.allowable_clefs)(['treble'])

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto flute.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> alto_flute = abjad.instrumenttools.AltoFlute()
                >>> f(alto_flute)
                instrumenttools.AltoFlute(
                    instrument_name='alto flute',
                    short_instrument_name='alt. fl.',
                    instrument_name_markup=abjad.Markup(
                        contents=['Alto flute'],
                        ),
                    short_instrument_name_markup=abjad.Markup(
                        contents=['Alt. fl.'],
                        ),
                    allowable_clefs=instrumenttools.ClefList(
                        [
                            abjad.Clef(
                                name='treble',
                                ),
                            ]
                        ),
                    pitch_range=abjad.PitchRange('[G3, G6]'),
                    sounding_pitch_of_written_middle_c=abjad.NamedPitch('g'),
                    )

        Returns string.
        '''
        superclass = super(AltoFlute, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets alto flute's allowable clefs.

        ..  container:: example

            ::

                >>> alto_flute.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(alto_flute.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets alto flute's name.

        ..  container:: example

            ::

                >>> alto_flute.instrument_name
                'alto flute'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets alto flute's instrument name markup.

        ..  container:: example

            ::

                >>> alto_flute.instrument_name_markup
                Markup(contents=['Alto flute'])

            ::

                >>> show(alto_flute.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets alto flute's range.

        ..  container:: example

            ::

                >>> alto_flute.pitch_range
                PitchRange('[G3, G6]')

            ::

                >>> show(alto_flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets alto flute's short instrument name.

        ..  container:: example

            ::

                >>> alto_flute.short_instrument_name
                'alt. fl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets alto flute's short instrument name markup.

        ..  container:: example

            ::

                >>> alto_flute.short_instrument_name_markup
                Markup(contents=['Alt. fl.'])

            ::

                >>> show(alto_flute.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of alto flute's written middle C.

        ..  container:: example

            ::

                >>> alto_flute.sounding_pitch_of_written_middle_c
                NamedPitch('g')

            ::

                >>> show(alto_flute.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
