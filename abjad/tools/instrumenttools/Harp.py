# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Harp(Instrument):
    r'''A harp.

    ::

        >>> staff_group = StaffGroup()
        >>> staff_group.context_name = 'PianoStaff'
        >>> staff_group.append(Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(Staff("c'2 b2"))
        >>> harp = instrumenttools.Harp()
        >>> attach(harp, staff_group)
        >>> attach(Clef(name='bass'), staff_group[1])
        >>> show(staff_group) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff_group))
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Harp }
            \set PianoStaff.shortInstrumentName = \markup { Hp. }
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                \clef "bass"
                c'2
                b2
            }
        >>

    The harp targets piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='harp',
        short_instrument_name='hp.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[B0, G#7]',
        sounding_pitch_of_written_middle_c=None,
        ):
        from abjad.tools import scoretools
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
        self._default_scope = 'PianoStaff'
        self._performer_names.extend([
            'string player',
            'harpist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets harp's allowable clefs.

        ..  container:: example

            ::

                >>> harp.allowable_clefs
                ClefInventory([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(harp.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets harp's name.

        ..  container:: example

            ::

                >>> harp.instrument_name
                'harp'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets harp's instrument name markup.

        ..  container:: example

            ::

                >>> harp.instrument_name_markup
                Markup(contents=('Harp',))

            ::

                >>> show(harp.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets harp's range.

        ..  container:: example

            ::

                >>> harp.pitch_range
                PitchRange(range_string='[B0, G#7]')

            ::

                >>> show(harp.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets harp's short instrument name.

        ..  container:: example

            ::

                >>> harp.short_instrument_name
                'hp.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets harp's short instrument name markup.

        ..  container:: example

            ::

                >>> harp.short_instrument_name_markup
                Markup(contents=('Hp.',))

            ::

                >>> show(harp.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of harp's written middle C.

        ..  container:: example

            ::

                >>> harp.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(harp.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
