from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.scoremanagementtools import specifiers


class Chunk(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        self._tempo = specifiers.TempoSpecifier()

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    ### PUBLIC METHODS ###

    def make(self):
        pass

    def make_empty_score(self):
        return scoretools.make_empty_piano_score()
