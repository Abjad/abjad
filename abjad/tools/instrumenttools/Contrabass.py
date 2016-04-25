# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabass(Instrument):
    r'''A contrabass.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> contrabass = instrumenttools.Contrabass()
        >>> attach(contrabass, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Contrabass }
            \set Staff.shortInstrumentName = \markup { Cb. }
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
        instrument_name='contrabass',
        short_instrument_name='cb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('bass', 'treble'),
        default_tuning=('C1', 'A1', 'D2', 'G2'),
        pitch_range='[C1, G4]',
        sounding_pitch_of_written_middle_c='C3',
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
            'contrabassist',
            'bassist',
            ])
        self._is_primary_instrument = True
        self._starting_clefs = indicatortools.ClefInventory(['bass'])
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets contrabass's allowable clefs.

        ..  container:: example

            ::

                >>> contrabass.allowable_clefs
                ClefInventory([Clef(name='bass'), Clef(name='treble')])

            ::

                >>> show(contrabass.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets contrabass's default tuning.

        ..  container:: example

            >>> contrabass.default_tuning
            Tuning(pitches=PitchSegment(['c,,', 'a,,', 'd,', 'g,']))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def instrument_name(self):
        r'''Gets contrabass's name.

        ..  container:: example

            ::

                >>> contrabass.instrument_name
                'contrabass'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets contrabass's instrument name markup.

        ..  container:: example

            ::

                >>> contrabass.instrument_name_markup
                Markup(contents=('Contrabass',))

            ::

                >>> show(contrabass.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass's range.

        ..  container:: example

            ::

                >>> contrabass.pitch_range
                PitchRange(range_string='[C1, G4]')

            ::

                >>> show(contrabass.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets contrabass's short instrument name.

        ..  container:: example

            ::

                >>> contrabass.short_instrument_name
                'cb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets contrabass's short instrument name markup.

        ..  container:: example

            ::

                >>> contrabass.short_instrument_name_markup
                Markup(contents=('Cb.',))

            ::

                >>> show(contrabass.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of contrabass's written middle C.

        ..  container:: example

            ::

                >>> contrabass.sounding_pitch_of_written_middle_c
                NamedPitch('c')

            ::

                >>> show(contrabass.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
