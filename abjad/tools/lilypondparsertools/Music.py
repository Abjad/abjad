# -*- coding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class Music(AbjadObject):
    r'''Abjad model of the LilyPond AST music node.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        'music',
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        self.music = music

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def construct(self):
        r'''Please document.
        '''
        raise NotImplementedError
