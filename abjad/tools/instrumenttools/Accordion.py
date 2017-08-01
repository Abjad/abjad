# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Accordion(Instrument):
    r'''Accordion.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff_group = abjad.StaffGroup()
            >>> staff_group.context_name = 'PianoStaff'
            >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
            >>> staff_group.append(abjad.Staff("c'2 b2"))
            >>> accordion = abjad.instrumenttools.Accordion()
            >>> abjad.attach(accordion, staff_group[0][0])
            >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
            >>> show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> f(staff_group)
            \new PianoStaff <<
                \new Staff {
                    \set PianoStaff.instrumentName = \markup { Accordion }
                    \set PianoStaff.shortInstrumentName = \markup { Acc. }
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

    The accordion targets the piano staff context by default.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='accordion',
        short_instrument_name='acc.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        pitch_range='[E1, C8]',
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
        self._default_scope = 'PianoStaff'
        self._performer_names.extend([
            'keyboardist',
            'accordionist',
            ])
        self._is_primary_instrument = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats accordion.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            ::

                >>> accordion = abjad.instrumenttools.Accordion()
                >>> f(accordion)
                instrumenttools.Accordion(
                    instrument_name='accordion',
                    short_instrument_name='acc.',
                    instrument_name_markup=abjad.Markup(
                        contents=['Accordion'],
                        ),
                    short_instrument_name_markup=abjad.Markup(
                        contents=['Acc.'],
                        ),
                    allowable_clefs=instrumenttools.ClefList(
                        [
                            abjad.Clef(
                                name='treble',
                                ),
                            abjad.Clef(
                                name='bass',
                                ),
                            ]
                        ),
                    pitch_range=abjad.PitchRange('[E1, C8]'),
                    sounding_pitch_of_written_middle_c=abjad.NamedPitch("c'"),
                    )

        Returns string.
        '''
        superclass = super(Accordion, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets accordion's allowable clefs.

        ..  container:: example

            ::

                >>> accordion.allowable_clefs
                ClefList([Clef(name='treble'), Clef(name='bass')])

            ::

                >>> show(accordion.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_scope(self):
        r'''Gets default scope of accordion.

        ..  container:: example

            ::

                >>> accordion.default_scope
                'PianoStaff'

        Returns piano staff.
        '''
        return self._default_scope

    @property
    def instrument_name(self):
        r'''Gets accordion's name.

        ..  container:: example

            ::

                >>> accordion.instrument_name
                'accordion'

        Returns string.
        '''
        return Instrument.instrument_name.fget(self)

    @property
    def instrument_name_markup(self):
        r'''Gets accordion's instrument name markup.

        ..  container:: example

            ::

                >>> accordion.instrument_name_markup
                Markup(contents=['Accordion'])

            ::

                >>> show(accordion.instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.instrument_name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets accordion's range.

        ..  container:: example

            ::

                >>> accordion.pitch_range
                PitchRange('[E1, C8]')

            ::

                >>> show(accordion.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_instrument_name(self):
        r'''Gets accordion's short instrument name.

        ..  container:: example

            ::

                >>> accordion.short_instrument_name
                'acc.'

        Returns string.
        '''
        return Instrument.short_instrument_name.fget(self)

    @property
    def short_instrument_name_markup(self):
        r'''Gets accordion's short instrument name markup.

        ..  container:: example

            ::

                >>> accordion.short_instrument_name_markup
                Markup(contents=['Acc.'])

            ::

                >>> show(accordion.short_instrument_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_instrument_name_markup.fget(self)

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of accordion's written middle C.

        ..  container:: example

            ::

                >>> accordion.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> show(accordion.sounding_pitch_of_written_middle_c) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
