# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class ClarinetInBFlat(Instrument):
    r'''A B-flat clarinet.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> clarinet = instrumenttools.ClarinetInBFlat()
        >>> attach(clarinet, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
            \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
            c'4
            d'4
            e'4
            fs'4
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'cl.'

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='clarinet in B-flat',
        short_instrument_name='cl. in B-flat',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[D3, Bb6]',
        sounding_pitch_of_written_middle_c='Bb3',
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
        self._is_primary_instrument = True

    ### PRIVATE METHODS ###

    def _get_performer_names(self):
        r'''Get performer names:

        ::

            >>> for performer_name in clarinet._get_performer_names():
            ...     performer_name
            'instrumentalist'
            'wind player'
            'reed player'
            'single reed player'
            'clarinettist'
            'clarinetist'

        Returns list.
        '''
        return super(ClarinetInBFlat, self)._get_performer_names()

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets clarinet in B-flat's allowable clefs.

        ..  container:: example

            ::

                >>> clarinet.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(clarinet.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets clarinet in B-flat's name.

        ..  container:: example

            ::

                >>> clarinet.instrument_name
                'clarinet in B-flat'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets clarinet in B-flat's instrument name markup.

        ..  container:: example

            ::

                >>> clarinet.instrument_name_markup
                Markup(contents=('Clarinet in B-flat',))

            ::

                >>> show(clarinet.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets clarinet in B-flat's range.

        ..  container:: example

            ::

                >>> clarinet.pitch_range
                PitchRange(range_string='[D3, Bb6]')

            ::

                >>> show(clarinet.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets clarinet in B-flat's short instrument name.

        ..  container:: example

            ::

                >>> clarinet.short_instrument_name
                'cl. in B-flat'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets clarinet in B-flat's short instrument name markup.

        ..  container:: example

            ::

                >>> clarinet.short_instrument_name_markup
                Markup(contents=('Cl. in B-flat',))

            ::

                >>> show(clarinet.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of clarinet in B-flat's written middle C.

        ..  container:: example

            ::

                >>> clarinet.sounding_pitch_of_written_middle_c
                NamedPitch('bf')

            ::

                >>> show(clarinet.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
