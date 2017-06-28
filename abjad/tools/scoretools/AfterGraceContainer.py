# -*- coding: utf-8 -*-
from abjad.tools.scoretools.GraceContainer import GraceContainer


class AfterGraceContainer(GraceContainer):
    r'''An after grace container.

    ..  container:: example

        After grace notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> notes = [Note("c'16"), Note("d'16")]
            >>> after_grace_container = AfterGraceContainer(notes)
            >>> attach(after_grace_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \afterGrace
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    Fill grace containers with notes, rests or chords.

    Attach after grace containers to notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    ### INITIALIZER ###

    def __init__(self, music=None):
        GraceContainer.__init__(self, music=music, kind='after')

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Deprecated.
        '''
        return self._kind

    @kind.setter
    def kind(self, arg):
        if arg not in self._allowable_kinds:
            message = 'unknown grace container kind: {!r}.'
            message = message.format(arg)
            raise Exception(message)
        self._kind = arg
