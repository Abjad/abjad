from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        from experimental import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        from experimental import quantizationtools
        def recurse(node):
            result = []
            for child in node.children:
                if isinstance(child, quantizationtools.QGridLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            return result
        return tuple(recurse(self))

