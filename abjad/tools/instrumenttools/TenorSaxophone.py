# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class TenorSaxophone(Instrument):
    r'''Tenor saxophone.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> tenor_saxophone = abjad.instrumenttools.TenorSaxophone()
            >>> abjad.attach(tenor_saxophone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Tenor saxophone" }
                \set Staff.shortInstrumentName = \markup { "Ten. sax." }
                c'4
                d'4
                e'4
                fs'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name='tenor saxophone',
        short_name='ten. sax.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        middle_c_sounding_pitch='Bb2',
        pitch_range='[Ab2, E5]',
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            middle_c_sounding_pitch=middle_c_sounding_pitch,
            pitch_range=pitch_range,
            )
        self._performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets tenor saxophone's allowable clefs.

        ..  container:: example

            ::

                >>> tenor_saxophone.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(tenor_saxophone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of tenor saxophone's written middle C.

        ..  container:: example

            ::

                >>> tenor_saxophone.middle_c_sounding_pitch
                NamedPitch('bf,')

            ::

                >>> show(tenor_saxophone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets tenor saxophone's name.

        ..  container:: example

            ::

                >>> tenor_saxophone.name
                'tenor saxophone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets tenor saxophone's instrument name markup.

        ..  container:: example

            ::

                >>> tenor_saxophone.name_markup
                Markup(contents=['Tenor saxophone'])

            ::

                >>> show(tenor_saxophone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets tenor saxophone's range.

        ..  container:: example

            ::

                >>> tenor_saxophone.pitch_range
                PitchRange('[Ab2, E5]')

            ::

                >>> show(tenor_saxophone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets tenor saxophone's short instrument name.

        ..  container:: example

            ::

                >>> tenor_saxophone.short_name
                'ten. sax.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets tenor saxophone's short instrument name markup.

        ..  container:: example

            ::

                >>> tenor_saxophone.short_name_markup
                Markup(contents=['Ten. sax.'])

            ::

                >>> show(tenor_saxophone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
