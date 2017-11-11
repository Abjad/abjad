from abjad.tools import indicatortools
from abjad.tools.instrumenttools.Instrument import Instrument


class Contrabass(Instrument):
    r'''Contrabass.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
        >>> clef = abjad.Clef('bass')
        >>> abjad.attach(clef, staff[0])
        >>> contrabass = abjad.Contrabass()
        >>> abjad.attach(contrabass, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Contrabass }
                \set Staff.shortInstrumentName = \markup { Cb. }
                \clef "bass"
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_tuning',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name='contrabass',
        short_name='cb.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass', 'treble'),
        context=None,
        default_tuning=('C1', 'A1', 'D2', 'G2'),
        middle_c_sounding_pitch='C3',
        pitch_range='[C1, G4]',
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
        self._default_tuning = indicatortools.Tuning(default_tuning)

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets contrabass's allowable clefs.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.allowable_clefs
            ('bass', 'treble')

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def default_tuning(self):
        r'''Gets contrabass's default tuning.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.default_tuning
            Tuning(pitches=PitchSegment(['c,,', 'a,,', 'd,', 'g,']))

        Returns tuning.
        '''
        return self._default_tuning

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of contrabass's written middle C.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.middle_c_sounding_pitch
            NamedPitch('c')

            >>> abjad.show(contrabass.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets contrabass's name.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.name
            'contrabass'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets contrabass's instrument name markup.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.name_markup
            Markup(contents=['Contrabass'])

            >>> abjad.show(contrabass.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets contrabass's range.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.pitch_range
            PitchRange('[C1, G4]')

            >>> abjad.show(contrabass.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets contrabass's short instrument name.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.short_name
            'cb.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets contrabass's short instrument name markup.

        ..  container:: example

            >>> contrabass = abjad.Contrabass()
            >>> contrabass.short_name_markup
            Markup(contents=['Cb.'])

            >>> abjad.show(contrabass.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
