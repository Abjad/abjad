# -*- coding: utf-8 -*-
from abjad.tools.scoretools.GraceContainer import GraceContainer


class AcciaccaturaContainer(GraceContainer):
    r'''An acciaccatura container.

    ..  container:: example

        Acciaccatura notes:

        ::

            >>> voice = Voice("c'4 d'4 e'4 f'4")
            >>> notes = [Note("c'16"), Note("d'16")]
            >>> acciaccatura_container = AcciaccaturaContainer(notes)
            >>> attach(acciaccatura_container, voice[1])
            >>> show(voice) # doctest: +SKIP

        ..  doctest::

            >>> f(voice)
            \new Voice {
                c'4
                \acciaccatura {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill acciaccatura containers with notes, rests or chords.

    Attach acciaccatura containers to notes, rests or chords.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    ### INITIALIZER ###

    def __init__(self, music=None):
        GraceContainer.__init__(self, music=music, kind='acciaccatura')

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
