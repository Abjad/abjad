# -*- coding: utf-8 -*-
from abjad.tools.scoretools.GraceContainer import GraceContainer


class AppoggiaturaContainer(GraceContainer):
    r'''An appoggiatura container.

    ..  container:: example

        Appoggiatura notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> notes = [Note("c'16"), Note("d'16")]
            >>> appoggiatura_container = AppoggiaturaContainer(notes)
            >>> attach(appoggiatura_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \appoggiatura {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill appoggiatura containers with notes, rests or chords.

    Attach appoggiatura containers to notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    ### INITIALIZER ###

    def __init__(self, music=None):
        GraceContainer.__init__(self, music=music, kind='appoggiatura')

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Deprecated.
        '''
        return self._kind

    @kind.setter
    def kind(self, argument):
        if argument not in self._allowable_kinds:
            message = 'unknown grace container kind: {!r}.'
            message = message.format(argument)
            raise Exception(message)
        self._kind = argument
