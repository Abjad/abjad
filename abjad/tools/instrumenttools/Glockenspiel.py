# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Glockenspiel(Instrument):
    r'''A glockenspiel.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> glockenspiel = instrumenttools.Glockenspiel()
        >>> attach(glockenspiel, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Glockenspiel }
            \set Staff.shortInstrumentName = \markup { Gkspl. }
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
        instrument_name='glockenspiel',
        short_instrument_name='gkspl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[G5, C8]',
        sounding_pitch_of_written_middle_c='C6',
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
            'percussionist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets glockenspiel's allowable clefs.

        ..  container:: example

            ::

                >>> glockenspiel.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(glockenspiel.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets glockenspiel's name.

        ..  container:: example

            ::

                >>> glockenspiel.instrument_name
                'glockenspiel'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets glockenspiel's instrument name markup.

        ..  container:: example

            ::

                >>> glockenspiel.instrument_name_markup
                Markup(contents=('Glockenspiel',))

            ::

                >>> show(glockenspiel.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets glockenspiel's range.

        ..  container:: example

            ::

                >>> glockenspiel.pitch_range
                PitchRange(range_string='[G5, C8]')

            ::

                >>> show(glockenspiel.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets glockenspiel's short instrument name.

        ..  container:: example

            ::

                >>> glockenspiel.short_instrument_name
                'gkspl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets glockenspiel's short instrument name markup.

        ..  container:: example

            ::

                >>> glockenspiel.short_instrument_name_markup
                Markup(contents=('Gkspl.',))

            ::

                >>> show(glockenspiel.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r"""Gets sounding pitch of glockenspiel's written middle C.

        ..  container:: example

            ::

                >>> glockenspiel.sounding_pitch_of_written_middle_c
                NamedPitch("c'''")

            ::

                >>> show(glockenspiel.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        """
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
