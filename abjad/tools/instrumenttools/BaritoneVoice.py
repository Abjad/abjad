from .Instrument import Instrument


class BaritoneVoice(Instrument):
    r'''Baritone voice.

    ..  container:: example

        >>> staff = abjad.Staff("c4 d4 e4 fs4")
        >>> baritone = abjad.BaritoneVoice()
        >>> abjad.attach(baritone, staff[0])
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Baritone }
                \set Staff.shortInstrumentName = \markup { Bar. }
                \clef "bass"
                c4
                d4
                e4
                fs4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(
        self,
        name='baritone',
        short_name='bar.',
        markup=None,
        short_markup=None,
        allowable_clefs=('bass',),
        context=None,
        middle_c_sounding_pitch=None,
        pitch_range='[A2, A4]',
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

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets baritone's allowable clefs.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.allowable_clefs
            ('bass',)

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def markup(self):
        r'''Gets baritone's instrument name markup.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.markup
            Markup(contents=['Baritone'])

            >>> abjad.show(baritone.markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.markup.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of baritone's written middle C.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.middle_c_sounding_pitch
            NamedPitch("c'")

            >>> abjad.show(baritone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets baritone's name.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.name
            'baritone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def pitch_range(self):
        r'''Gets baritone's range.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.pitch_range
            PitchRange('[A2, A4]')

            >>> abjad.show(baritone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_markup(self):
        r'''Gets baritone's short instrument name markup.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.short_markup
            Markup(contents=['Bar.'])

            >>> abjad.show(baritone.short_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_markup.fget(self)

    @property
    def short_name(self):
        r'''Gets baritone's short instrument name.

        ..  container:: example

            >>> baritone = abjad.BaritoneVoice()
            >>> baritone.short_name
            'bar.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)
