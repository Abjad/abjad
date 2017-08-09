# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class Glockenspiel(Instrument):
    r'''Glockenspiel.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 fs'4")
            >>> glockenspiel = abjad.instrumenttools.Glockenspiel()
            >>> abjad.attach(glockenspiel, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                \set Staff.instrumentName = \markup { Glockenspiel }
                \set Staff.shortInstrumentName = \markup { Gkspl. }
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
        name='glockenspiel',
        short_name='gkspl.',
        name_markup=None,
        short_name_markup=None,
        allowable_clefs=None,
        middle_c_sounding_pitch='C6',
        pitch_range='[G5, C8]',
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
            'percussionist',
            ])

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets glockenspiel's allowable clefs.

        ..  container:: example

            ::

                >>> glockenspiel.allowable_clefs
                ClefList([Clef(name='treble')])

            ::

                >>> show(glockenspiel.allowable_clefs) # doctest: +SKIP

        Returns clef list.
        '''
        return Instrument.allowable_clefs.fget(self)

    @property
    def middle_c_sounding_pitch(self):
        r"""Gets sounding pitch of glockenspiel's written middle C.

        ..  container:: example

            ::

                >>> glockenspiel.middle_c_sounding_pitch
                NamedPitch("c'''")

            ::

                >>> show(glockenspiel.middle_c_sounding_pitch) # doctest: +SKIP

        Returns named pitch.
        """
        return Instrument.middle_c_sounding_pitch.fget(self)

    @property
    def name(self):
        r'''Gets glockenspiel's name.

        ..  container:: example

            ::

                >>> glockenspiel.name
                'glockenspiel'

        Returns string.
        '''
        return Instrument.name.fget(self)

    @property
    def name_markup(self):
        r'''Gets glockenspiel's instrument name markup.

        ..  container:: example

            ::

                >>> glockenspiel.name_markup
                Markup(contents=['Glockenspiel'])

            ::

                >>> show(glockenspiel.name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.name_markup.fget(self)

    @property
    def pitch_range(self):
        r'''Gets glockenspiel's range.

        ..  container:: example

            ::

                >>> glockenspiel.pitch_range
                PitchRange('[G5, C8]')

            ::

                >>> show(glockenspiel.pitch_range) # doctest: +SKIP

        Returns pitch range.
        '''
        return Instrument.pitch_range.fget(self)

    @property
    def short_name(self):
        r'''Gets glockenspiel's short instrument name.

        ..  container:: example

            ::

                >>> glockenspiel.short_name
                'gkspl.'

        Returns string.
        '''
        return Instrument.short_name.fget(self)

    @property
    def short_name_markup(self):
        r'''Gets glockenspiel's short instrument name markup.

        ..  container:: example

            ::

                >>> glockenspiel.short_name_markup
                Markup(contents=['Gkspl.'])

            ::

                >>> show(glockenspiel.short_name_markup) # doctest: +SKIP

        Returns markup.
        '''
        return Instrument.short_name_markup.fget(self)
