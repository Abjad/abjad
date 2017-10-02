from abjad.tools.instrumenttools.Instrument import Instrument


class Harp(Instrument):
    r'''Harp.

    ..  container:: example

        ::

            >>> staff_group = abjad.StaffGroup(context_name='PianoStaff')
            >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
            >>> staff_group.append(abjad.Staff("c'2 b2"))
            >>> harp = abjad.Harp()
            >>> abjad.attach(harp, staff_group[0][0])
            >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
            >>> show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> f(staff_group)
            \new PianoStaff <<
                \new Staff {
                    \set PianoStaff.instrumentName = \markup { Harp }
                    \set PianoStaff.shortInstrumentName = \markup { Hp. }
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
        name='harp',
        short_name='hp.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('treble', 'bass'),
        default_scope='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[B0, G#7]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            default_scope=default_scope,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets harp's allowable clefs.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.allowable_clefs
                ('treble', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_scope(self):
        r'''Gets default scope of harp.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.default_scope
                'StaffGroup'

        Returns piano staff.
        '''
        return self._default_scope

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of harp's written middle C.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(harp.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets harp's name.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.name
                'harp'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets harp's instrument name markup.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.name_markup
                Markup(contents=['Harp'])

            ::

                >>> show(harp.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets harp's range.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.pitch_range
                PitchRange('[B0, G#7]')

            ::

                >>> show(harp.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets harp's short instrument name.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.short_name
                'hp.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets harp's short instrument name markup.

        ..  container:: example

            ::

                >>> harp = abjad.Harp()
                >>> harp.short_name_markup
                Markup(contents=['Hp.'])

            ::

                >>> show(harp.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
