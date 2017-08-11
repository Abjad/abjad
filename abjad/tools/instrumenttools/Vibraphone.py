# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Vibraphone(Instrument):
    r'''Vibraphone.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> vibraphone = abjad.instrumenttools.Vibraphone()
            >>> abjad.attach(vibraphone, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Vibraphone }
                \set Staff.shortInstrumentName = \markup { Vibr. }
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
        name='vibraphone',
        short_name='vibr.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        pitch_range='[F3, F6]',
        middle_c_sounding_pitch=None,
        ):
        Instrument.__init__(
            self,
            name=name,
            short_name=short_name,
            name_markup=name_markup,
            short_name_markup=short_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            middle_c_sounding_pitch=\
                middle_c_sounding_pitch,
            )
        self._performer_names.extend([
            'percussionist',
            'vibraphonist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets vibraphone's allowable clefs.

        ..  container:: example

            ::

                >>> vibraphone.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(vibraphone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of vibraphone's written middle C.

        ..  container:: example

            ::

                >>> vibraphone.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(vibraphone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets vibraphone's name.

        ..  container:: example

            ::

                >>> vibraphone.name
                'vibraphone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets vibraphone's instrument name markup.

        ..  container:: example

            ::

                >>> vibraphone.name_markup
                Markup(contents=['Vibraphone'])

            ::

                >>> show(vibraphone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets vibraphone's range.

        ..  container:: example

            ::

                >>> vibraphone.pitch_range
                PitchRange('[F3, F6]')

            ::

                >>> show(vibraphone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets vibraphone's short instrument name.

        ..  container:: example

            ::

                >>> vibraphone.short_name
                'vibr.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets vibraphone's short instrument name markup.

        ..  container:: example

            ::

                >>> vibraphone.short_name_markup
                Markup(contents=['Vibr.'])

            ::

                >>> show(vibraphone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
