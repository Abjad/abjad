from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):
    '''Statal server.
    '''

    ### INITIALIZER ###

    def __init__(self, iterable):
        self.iterable = sequencetools.CyclicTuple(iterable)
        self.next_index = 0

    ### SPECIAL METHODS ###

    def __call__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def last_node(self):
        '''Statal server last node.
        '''
        return self.last_nodes[-1]
