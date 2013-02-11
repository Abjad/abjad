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

    def __call__(self, expression):
        '''Evaluate `expression` against statal server.

        Return payload expression.
        '''
        result = []
        assert not (expression.count is not None and expression.index is not None)
        if expression.count is not None:
            for x in range(expression.count):
                result.append(self.iterable[self.next_index])
                self.next_index += 1
        elif expression.index is not None:
            result.append(self.iterable[expression.index])
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def last_node(self):
        '''Statal server last node.
        '''
        return self.last_nodes[-1]
