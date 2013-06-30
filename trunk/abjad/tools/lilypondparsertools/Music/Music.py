import abc
from abjad.tools.abctools import AbjadObject


class Music(AbjadObject):
    '''Abjad model of the LilyPond AST music node.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        'music',
        )

    ### INITIALIZER ###

    def __init__(self, music):
        self.music = music

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def construct(self):
        raise NotImplemented
