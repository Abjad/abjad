# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.lilypondparsertools.Music import Music


class SequentialMusic(Music):
    r'''Abjad model of the LilyPond AST sequential music node.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def construct(self):
        r'''Constructs sequential music.

        Returns Abjad container.
        '''
        from abjad.tools import lilypondparsertools
        container = scoretools.Container([])
        for x in self.music:
            if isinstance(x, scoretools.Component):
                container.append(x)
            elif isinstance(x, type(self)):
                container.extend(x.construct())
        return container
