# -*- coding: utf-8 -*-
from abjad.tools.scoretools.Context import Context


class Voice(Context):
    r'''Voice.

    ..  container:: example

        ::

            >>> voice = Voice("c'8 d'8 e'8 f'8")
            >>> show(voice) # doctest: +SKIP

        ..  docs::

            >>> f(voice)
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = (
        )

    _default_context_name = 'Voice'

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='Voice', name=None):
        Context.__init__(
            self,
            music=music,
            context_name=context_name,
            name=name,
            )
