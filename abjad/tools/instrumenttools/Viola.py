# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Viola(Instrument):
    r'''A viola.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='alto')
        >>> attach(clef, staff)
        >>> viola = instrumenttools.Viola()
        >>> attach(viola, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "alto"
            \set Staff.instrumentName = \markup { Viola }
            \set Staff.shortInstrumentName = \markup { Va. }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='viola',
        short_instrument_name='va.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('alto', 'treble'),
        default_tuning=('C3', 'G3', 'D4', 'A4'),
        pitch_range='[C3, D6]',
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
            'string player',
            'violist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['alto'])
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets viola's allowable clefs.

        ..  container:: example

            ::

                >>> viola.allowable_clefs
                ClefInventory([Clef(name='alto'), Clef(name='treble')])

            ::

                >>> show(viola.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets viola's default tuning.

        ..  container:: example

            >>> viola.default_tuning
            Tuning(pitches=PitchSegment(['c', 'g', "d'", "a'"]))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def instrument_name(self):
        r'''Gets viola's name.

        ..  container:: example

            ::

                >>> viola.instrument_name
                'viola'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets viola's instrument name markup.

        ..  container:: example

            ::

                >>> viola.instrument_name_markup
                Markup(contents=('Viola',))

            ::

                >>> show(viola.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets viola's range.

        ..  container:: example

            ::

                >>> viola.pitch_range
                PitchRange(range_string='[C3, D6]')

            ::

                >>> show(viola.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets viola's short instrument name.

        ..  container:: example

            ::

                >>> viola.short_instrument_name
                'va.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets viola's short instrument name markup.

        ..  container:: example

            ::

                >>> viola.short_instrument_name_markup
                Markup(contents=('Va.',))

            ::

                >>> show(viola.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of viola's written middle C.

        ..  container:: example

            ::

                >>> viola.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(viola.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
