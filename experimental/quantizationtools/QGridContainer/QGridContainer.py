from abjad.tools import rhythmtreetools
from experimental.quantizationtools.QGridLeaf import QGridLeaf


class QGridContainer(rhythmtreetools.RhythmTreeContainer):

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        return (type(self), QGridLeaf)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        def recurse(node):
            result = []
            for child in node.children:
                if isinstance(child, QGridLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            return result
        return tuple(recurse(self))

