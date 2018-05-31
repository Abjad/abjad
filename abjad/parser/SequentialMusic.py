from abjad import core
from .Music import Music


class SequentialMusic(Music):
    """
    Abjad model of the LilyPond AST sequential music node.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    def construct(self):
        """
        Constructs sequential music.

        Returns Abjad container.
        """
        container = core.Container()
        for x in self.music:
            if isinstance(x, core.Component):
                container.append(x)
            elif isinstance(x, type(self)):
                container.extend(x.construct())
        return container
