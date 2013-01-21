from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StatalServer(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, iterable):
        self.iterable = sequencetools.CyclicTuple(iterable)
        self.next_index = 0

    ### SPECIAL METHODS ###

    def __call__(self, request):
        result = []
        assert not (request.count is not None and request.index is not None)
        if request.count is not None:
            for x in range(request.count):
                result.append(self.iterable[self.next_index])
                self.next_index += 1
        elif request.index is not None:
            result.append(self.iterable[request.index])
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def last_node(self):
        return self.last_nodes[-1]
