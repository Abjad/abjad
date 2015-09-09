# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Xylophone(Instrument):
    r'''A xylphone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 fs'4")
        >>> xylophone = instrumenttools.Xylophone()
        >>> attach(xylophone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff))
        \new Staff {
            \set Staff.instrumentName = \markup { Xylophone }
            \set Staff.shortInstrumentName = \markup { Xyl. }
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
        instrument_name='xylophone',
        short_instrument_name='xyl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range='[C4, C7]',
        sounding_pitch_of_written_middle_c='C5',
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
            'xylophonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets xylophone's allowable clefs.

        ..  container:: example

            ::

                >>> xylophone.allowable_clefs
                ClefInventory([Clef(name='treble')])

            ::

                >>> show(xylophone.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets xylophone's name.

        ..  container:: example

            ::

                >>> xylophone.instrument_name
                'xylophone'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets xylophone's instrument name markup.

        ..  container:: example

            ::

                >>> xylophone.instrument_name_markup
                Markup(contents=('Xylophone',))

            ::

                >>> show(xylophone.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets xylophone's range.

        ..  container:: example

            ::

                >>> xylophone.pitch_range
                PitchRange(range_string='[C4, C7]')

            ::

                >>> show(xylophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets xylophone's short instrument name.

        ..  container:: example

            ::

                >>> xylophone.short_instrument_name
                'xyl.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets xylophone's short instrument name markup.

        ..  container:: example

            ::

                >>> xylophone.short_instrument_name_markup
                Markup(contents=('Xyl.',))

            ::

                >>> show(xylophone.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of xylophone's written middle C.

        ..  container:: example

            ::

                >>> xylophone.sounding_pitch_of_written_middle_c
                NamedPitch("c''")

            ::

                >>> show(xylophone.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
