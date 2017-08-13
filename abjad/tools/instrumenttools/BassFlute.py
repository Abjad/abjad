# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class BassFlute(Instrument):
    r'''Bass flute.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> bass_flute = abjad.instrumenttools.BassFlute()
            >>> abjad.attach(bass_flute, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { "Bass flute" }
                \set Staff.shortInstrumentName = \markup { "Bass fl." }
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
        name='bass flute',
        short_name='bass fl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        pitch_range='[C3, C6]',
        middle_c_sounding_pitch='C3',
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
            'wind player',
            'flautist',
            'flutist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets bass flute's allowable clefs.

        ..  container:: example

            ::

                >>> bass_flute.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(bass_flute.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r'''Gets sounding pitch of bass_flute's written middle C.

        ..  container:: example

            ::

                >>> bass_flute.middle_c_sounding_pitch
                NamedPitch('c')

            ::

                >>> show(bass_flute.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        '''
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets bass flute's name.

        ..  container:: example

            ::

                >>> bass_flute.name
                'bass flute'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets bass flute's instrument name markup.

        ..  container:: example

            ::

                >>> bass_flute.name_markup
                Markup(contents=['Bass flute'])

            ::

                >>> show(bass_flute.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets bass flute's range.

        ..  container:: example

            ::

                >>> bass_flute.pitch_range
                PitchRange('[C3, C6]')

            ::

                >>> show(bass_flute.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets bass flute's short instrument name.

        ..  container:: example

            ::

                >>> bass_flute.short_name
                'bass fl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets bass flute's short instrument name markup.

        ..  container:: example

            ::

                >>> bass_flute.short_name_markup
                Markup(contents=['Bass fl.'])

            ::

                >>> show(bass_flute.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
