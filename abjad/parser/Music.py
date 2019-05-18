import abc


class Music(object):
    """
    Abjad model of the LilyPond AST music node.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("music",)

    ### INITIALIZER ###

    def __init__(self, music=None):
        self.music = music

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def construct(self):
        """
        Please document.
        """
        raise NotImplementedError
