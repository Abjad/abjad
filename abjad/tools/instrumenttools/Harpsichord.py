from abjad.tools.instrumenttools.Instrument import Instrument


class Harpsichord(Instrument):
    r'''Harpsichord.

    ..  container:: example

        >>> upper_staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> lower_staff = abjad.Staff("c'2 b2")
        >>> staff_group = abjad.StaffGroup(
        ...     [upper_staff, lower_staff],
        ...     context_name='PianoStaff',
        ...     )
        >>> harpsichord = abjad.Harpsichord()
        >>> abjad.attach(harpsichord, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), lower_staff[0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
            \new PianoStaff <<
                \new Staff {
                    \set PianoStaff.instrumentName = \markup { Harpsichord }
                    \set PianoStaff.shortInstrumentName = \markup { Hpschd. }
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
        name='harpsichord',
        short_name='hpschd.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[C2, C7]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets harpsichord's allowable clefs.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.allowable_clefs
            ('treble', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def context(self):
        r'''Gets default context of harpsichord.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.context
            'StaffGroup'

        Returns piano staff.
        '''
        return self._context

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of harpsichord's written middle C.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(harpsichord.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets harpsichord's name.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.name
            'harpsichord'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets harpsichord's instrument name markup.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.name_markup
            Markup(contents=['Harpsichord'])

            >>> abjad.show(harpsichord.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets harpsichord's range.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.pitch_range
            PitchRange('[C2, C7]')

            >>> abjad.show(harpsichord.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets harpsichord's short instrument name.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.short_name
            'hpschd.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets harpsichord's short instrument name markup.

        ..  container:: example

            >>> harpsichord = abjad.Harpsichord()
            >>> harpsichord.short_name_markup
            Markup(contents=['Hpschd.'])

            >>> abjad.show(harpsichord.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
