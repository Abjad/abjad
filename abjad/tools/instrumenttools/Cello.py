# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Cello(Instrument):
    r'''A cello.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> cello = instrumenttools.Cello()
        >>> attach(cello, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Cello }
            \set Staff.shortInstrumentName = \markup { Vc. }
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
        instrument_name='cello',
        short_instrument_name='vc.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'tenor', 'treble'),
        default_tuning=('C2', 'G2', 'D3', 'A3'),
        pitch_range='[C2, G5]',
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
            'cellist',
            ])
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
        self._is_primary_instrument = True
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets cello's allowable clefs.

        ..  container:: example

            ::

                >>> cello.allowable_clefs
                ClefInventory([Clef(name='bass'), Clef(name='tenor'), Clef(name='treble')])

            ::

                >>> show(cello.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets cello's default tuning.

        ..  container:: example

            >>> cello.default_tuning
            Tuning(pitches=PitchSegment(['c,', 'g,', 'd', 'a']))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def instrument_name(self):
        r'''Gets cello's name.

        ..  container:: example

            ::

                >>> cello.instrument_name
                'cello'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets cello's instrument name markup.

        ..  container:: example

            ::

                >>> cello.instrument_name_markup
                Markup(contents=('Cello',))

            ::

                >>> show(cello.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets cello's range.

        ..  container:: example

            ::

                >>> cello.pitch_range
                PitchRange(range_string='[C2, G5]')

            ::

                >>> show(cello.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets cello's short instrument name.

        ..  container:: example

            ::

                >>> cello.short_instrument_name
                'vc.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets cello's short instrument name markup.

        ..  container:: example

            ::

                >>> cello.short_instrument_name_markup
                Markup(contents=('Vc.',))

            ::

                >>> show(cello.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of cello's written middle C.

        ..  container:: example

            ::

                >>> cello.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(cello.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
