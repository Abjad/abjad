from abjad.tools.instrumenttools.Instrument import Instrument


class Piano(Instrument):
    r'''Piano.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(context_name='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> piano = abjad.Piano()
        >>> abjad.attach(piano, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
            \new PianoStaff <<
                \new Staff {
                    \set PianoStaff.instrumentName = \markup { Piano }
                    \set PianoStaff.shortInstrumentName = \markup { Pf. }
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
        name='piano',
        short_name='pf.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[A0, C8]',
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
        r'''Gets piano's allowable clefs.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.allowable_clefs
            ('treble', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def context(self):
        r'''Gets default context of piano.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.context
            'StaffGroup'

        Return staff group.
        '''
        return self._context

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of piano's written middle C.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(piano.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets piano's name.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.name
            'piano'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets piano's instrument name markup.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.name_markup
            Markup(contents=['Piano'])

            >>> abjad.show(piano.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets piano's range.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.pitch_range
            PitchRange('[A0, C8]')

            >>> abjad.show(piano.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets piano's short instrument name.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.short_name
            'pf.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets piano's short instrument name markup.

        ..  container:: example

            >>> piano = abjad.Piano()
            >>> piano.short_name_markup
            Markup(contents=['Pf.'])

            >>> abjad.show(piano.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
