from .Instrument import Instrument


class Harp(Instrument):
    r'''Harp.

    ..  container:: example

        >>> staff_group = abjad.StaffGroup(lilypond_type='PianoStaff')
        >>> staff_group.append(abjad.Staff("c'4 d'4 e'4 f'4"))
        >>> staff_group.append(abjad.Staff("c'2 b2"))
        >>> harp = abjad.Harp()
        >>> abjad.attach(harp, staff_group[0][0])
        >>> abjad.attach(abjad.Clef('bass'), staff_group[1][0])
        >>> abjad.show(staff_group) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff_group)
            \new PianoStaff
            <<
                \new Staff
                {
                    \set PianoStaff.instrumentName = \markup { Harp }
                    \set PianoStaff.shortInstrumentName = \markup { Hp. }
                    c'4
                    d'4
                    e'4
                    f'4
                }
                \new Staff
                {
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
        *,
        name='harp',
        short_name='hp.',
        markup=None,
        short_markup=None,
        allowable_clefs=('treble', 'bass'),
        context='StaffGroup',
        middle_c_sounding_pitch=None,
        pitch_range='[B0, G#7]',
        hide=None,
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            markup=markup,
            short_markup=short_markup,
            allowable_clefs=allowable_clefs,
            context=context,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            hide=hide,
            )
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets harp's allowable clefs.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.allowable_clefs
            ('treble', 'bass')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def context(self):
        r'''Gets (historically conventional) context.

        ..  container:: example

            >>> abjad.Harp().context
            'StaffGroup'

        Returns ``'StaffGroup'``.

        Override with ``abjad.attach(..., context='...')``.
        '''
        return self._context

    @property
    def markup(self):
        r'''Gets harp's instrument name markup.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.markup
            Markup(contents=['Harp'])

            >>> abjad.show(harp.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of harp's written middle C.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(harp.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets harp's name.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.name
            'harp'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets harp's range.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.pitch_range
            PitchRange('[B0, G#7]')

            >>> abjad.show(harp.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets harp's short instrument name markup.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.short_markup
            Markup(contents=['Hp.'])

            >>> abjad.show(harp.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets harp's short instrument name.

        ..  container:: example

            >>> harp = abjad.Harp()
            >>> harp.short_name
            'hp.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
