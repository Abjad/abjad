from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools.lilypondparsertools.Music import Music


class SequentialMusic(Music):
    r'''Abjad model of the LilyPond AST sequential music node.
    '''

    ### PUBLIC METHODS ###

    def construct(self):
        from abjad.tools import lilypondparsertools
        container = containertools.Container([])
        for x in self.music:
            if isinstance(x, componenttools.Component):
                container.append(x)
            elif isinstance(x, type(self)):
                container.extend(x.construct())
        return container
