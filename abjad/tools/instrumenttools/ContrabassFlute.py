# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassFlute(Instrument):
    r'''A contrabass flute.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_flute = instrumenttools.ContrabassFlute()
        >>> attach(contrabass_flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "Contrabass flute" }
            \set Staff.shortInstrumentName = \markup { "Cbass. fl." }
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
        instrument_name='contrabass flute',
        short_instrument_name='cbass. fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[G2, G5]',
        sounding_pitch_of_written_middle_c='G2',
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

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets contrabass flute's allowable clefs.

        ..  container:: example

            ::

                >>> contrabass_flute.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(contrabass_flute.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets contrabass flute's name.

        ..  container:: example

            ::

                >>> contrabass_flute.instrument_name
                'contrabass flute'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets contrabass flute's instrument name markup.

        ..  container:: example

            ::

                >>> contrabass_flute.instrument_name_markup
                Markup(contents=('Contrabass flute',))

            ::

                >>> show(contrabass_flute.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass flute's range.

        ..  container:: example

            ::

                >>> contrabass_flute.pitch_range
                PitchRange(range_string='[G2, G5]')

            ::

                >>> show(contrabass_flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets contrabass flute's short instrument name.

        ..  container:: example

            ::

                >>> contrabass_flute.short_instrument_name
                'cbass. fl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets contrabass flute's short instrument name markup.

        ..  container:: example

            ::

                >>> contrabass_flute.short_instrument_name_markup
                Markup(contents=('Cbass. fl.',))

            ::

                >>> show(contrabass_flute.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of contrabass_flute's written middle C.

        ..  container:: example

            ::

                >>> contrabass_flute.sounding_pitch_of_written_middle_c
                NamedPitch('g,')

            ::

                >>> show(contrabass_flute.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
