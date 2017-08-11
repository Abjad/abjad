# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BaritoneVoice(Instrument):
    r'''Baritone voice.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c4 d4 e4 fs4")
            >>> baritone = abjad.instrumenttools.BaritoneVoice()
            >>> abjad.attach(baritone, staff[0])
            >>> clef = abjad.Clef('bass')
            >>> abjad.attach(clef, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
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

    __slots__ = (
        )

    performer_abbreviation = 'bar.'

    ### INITIALIZER ###

    def __init__(
        self,
        name='baritone',
        short_name='bar.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=('bass',),
        pitch_range='[A2, A4]',
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
            'vocalist',
            'baritone',
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets baritone's allowable clefs.

        ..  container:: example

            ::

                >>> baritone.allowable_clefs
                ClefList([Clef(name='bass')])

            ::

                >>> show(baritone.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of baritone's written middle C.

        ..  container:: example

            ::

                >>> baritone.middle_c_sounding_pitch
                NamedPitch("c'")

            ::

                >>> show(baritone.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets baritone's name.

        ..  container:: example

            ::

                >>> baritone.name
                'baritone'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets baritone's instrument name markup.

        ..  container:: example

            ::

                >>> baritone.name_markup
                Markup(contents=['Baritone'])

            ::

                >>> show(baritone.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets baritone's range.

        ..  container:: example

            ::

                >>> baritone.pitch_range
                PitchRange('[A2, A4]')

            ::

                >>> show(baritone.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets baritone's short instrument name.

        ..  container:: example

            ::

                >>> baritone.short_name
                'bar.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets baritone's short instrument name markup.

        ..  container:: example

            ::

                >>> baritone.short_name_markup
                Markup(contents=['Bar.'])

            ::

                >>> show(baritone.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
