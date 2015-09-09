# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Piano(Instrument):
    r'''A piano.

    ::

        >>> staff_group = StaffGroup()
        >>> staff_group.context_name = 'PianoStaff'
        >>> staff_group.append(Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(Staff("c'2 b2"))
        >>> piano = instrumenttools.Piano()
        >>> attach(piano, staff_group)
        >>> attach(Clef(name='bass'), staff_group[1])
        >>> show(staff_group) # doctest: +SKIP

    ..  doctest::

        >>> print(format(staff_group))
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Piano }
            \set PianoStaff.shortInstrumentName = \markup { Pf. }
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

    The piano targets piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='piano',
        short_instrument_name='pf.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[A0, C8]',
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
            'pianist',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets piano's allowable clefs.

        ..  container:: example

            ::

                >>> piano.allowable_clefs
                ClefInventory([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(piano.allowable_clefs) # doctest: +SKIP

        Returns clef inventory.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def instrument_name(self):
        r'''Gets piano's name.

        ..  container:: example

            ::

                >>> piano.instrument_name
                'piano'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets piano's instrument name markup.

        ..  container:: example

            ::

                >>> piano.instrument_name_markup
                Markup(contents=('Piano',))

            ::

                >>> show(piano.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets piano's range.

        ..  container:: example

            ::

                >>> piano.pitch_range
                PitchRange(range_string='[A0, C8]')

            ::

                >>> show(piano.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets piano's short instrument name.

        ..  container:: example

            ::

                >>> piano.short_instrument_name
                'pf.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets piano's short instrument name markup.

        ..  container:: example

            ::

                >>> piano.short_instrument_name_markup
                Markup(contents=('Pf.',))

            ::

                >>> show(piano.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of piano's written middle C.

        ..  container:: example

            ::

                >>> piano.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(piano.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
