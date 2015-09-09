# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Harpsichord(Instrument):
    r'''A harpsichord.

    ::

        >>> upper_staff = Staff("c'4 d'4 e'4 f'4")
        >>> lower_staff = Staff("c'2 b2")
        >>> staff_group = StaffGroup([upper_staff, lower_staff])
        >>> staff_group.context_name = 'PianoStaff'
        >>> harpsichord = instrumenttools.Harpsichord()
        >>> attach(harpsichord, staff_group)
        >>> attach(Clef(name='bass'), lower_staff)
        >>> show(staff_group) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff_group))
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Harpsichord }
            \set PianoStaff.shortInstrumentName = \markup { Hpschd. }
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

    The harpsichord targets piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='harpsichord',
        short_instrument_name='hpschd.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[C2, C7]',
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
            'keyboardist',
            'harpsichordist'
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets harpsichord's allowable clefs.

        ..  container:: example

            ::

                >>> harpsichord.allowable_clefs
                ClefInventory([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(harpsichord.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets harpsichord's name.

        ..  container:: example

            ::

                >>> harpsichord.instrument_name
                'harpsichord'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets harpsichord's instrument name markup.

        ..  container:: example

            ::

                >>> harpsichord.instrument_name_markup
                Markup(contents=('Harpsichord',))

            ::

                >>> show(harpsichord.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets harpsichord's range.

        ..  container:: example

            ::

                >>> harpsichord.pitch_range
                PitchRange(range_string='[C2, C7]')

            ::

                >>> show(harpsichord.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets harpsichord's short instrument name.

        ..  container:: example

            ::

                >>> harpsichord.short_instrument_name
                'hpschd.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets harpsichord's short instrument name markup.

        ..  container:: example

            ::

                >>> harpsichord.short_instrument_name_markup
                Markup(contents=('Hpschd.',))

            ::

                >>> show(harpsichord.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of harpsichord's written middle C.

        ..  container:: example

            ::

                >>> harpsichord.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(harpsichord.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
