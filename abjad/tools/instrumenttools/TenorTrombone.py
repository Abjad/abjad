# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorTrombone(Instrument):
    r'''A tenor trombone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clef = Clef(name='bass')
        >>> attach(clef, staff)
        >>> tenor_trombone = instrumenttools.TenorTrombone()
        >>> attach(tenor_trombone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Tenor trombone }
            \set Staff.shortInstrumentName = \markup { Ten. trb. }
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
        instrument_name='tenor trombone',
        short_instrument_name='ten. trb.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('tenor', 'bass'),
        pitch_range='[E2, Eb5]',
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
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tenor trombone's allowable clefs.

        ..  container:: example

            ::

                >>> tenor_trombone.allowable_clefs
                ClefInventory([Clef(name='tenor'), Clef(name='bass')])

            ::

                >>> show(tenor_trombone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets tenor trombone's name.

        ..  container:: example

            ::

                >>> tenor_trombone.instrument_name
                'tenor trombone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets tenor trombone's instrument name markup.

        ..  container:: example

            ::

                >>> tenor_trombone.instrument_name_markup
                Markup(contents=('Tenor trombone',))

            ::

                >>> show(tenor_trombone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor trombone's range.

        ..  container:: example

            ::

                >>> tenor_trombone.pitch_range
                PitchRange(range_string='[E2, Eb5]')

            ::

                >>> show(tenor_trombone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets tenor trombone's short instrument name.

        ..  container:: example

            ::

                >>> tenor_trombone.short_instrument_name
                'ten. trb.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets tenor trombone's short instrument name markup.

        ..  container:: example

            ::

                >>> tenor_trombone.short_instrument_name_markup
                Markup(contents=('Ten. trb.',))

            ::

                >>> show(tenor_trombone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of tenor trombone's written middle C.

        ..  container:: example

            ::

                >>> tenor_trombone.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(tenor_trombone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
