# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ContrabassClarinet(Instrument):
    r'''A contrassbass clarinet.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> contrabass_clarinet = instrumenttools.ContrabassClarinet()
        >>> attach(contrabass_clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "Contrabass clarinet" }
            \set Staff.shortInstrumentName = \markup { "Cbass. cl." }
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
        instrument_name='contrabass clarinet',
        short_instrument_name='cbass. cl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[Bb0, G4]',
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
            'clarinettist',
            'clarinetist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets contrabass clarinet's allowable clefs.

        ..  container:: example

            ::

                >>> contrabass_clarinet.allowable_clefs
                ClefInventory([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(contrabass_clarinet.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets contrabass clarinet's name.

        ..  container:: example

            ::

                >>> contrabass_clarinet.instrument_name
                'contrabass clarinet'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets contrabass clarinet's instrument name markup.

        ..  container:: example

            ::

                >>> contrabass_clarinet.instrument_name_markup
                Markup(contents=('Contrabass clarinet',))

            ::

                >>> show(contrabass_clarinet.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass clarinet's range.

        ..  container:: example

            ::

                >>> contrabass_clarinet.pitch_range
                PitchRange(range_string='[Bb0, G4]')

            ::

                >>> show(contrabass_clarinet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets contrabass clarinet's short instrument name.

        ..  container:: example

            ::

                >>> contrabass_clarinet.short_instrument_name
                'cbass. cl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets contrabass clarinet's short instrument name markup.

        ..  container:: example

            ::

                >>> contrabass_clarinet.short_instrument_name_markup
                Markup(contents=('Cbass. cl.',))

            ::

                >>> show(contrabass_clarinet.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of contrabass_clarinet's written middle C.

        ..  container:: example

            ::

                >>> contrabass_clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('bf,,')

            ::

                >>> show(contrabass_clarinet.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
