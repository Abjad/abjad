from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    '''A container in a ``QGrid`` structure:

    ::

        >>> container = quantizationtools.QGridContainer()

    ::

        >>> container
        QGridContainer(
            duration=Duration(1, 1)
            )

    Used internally by ``QGrid``.

    Return ``QGridContainer`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    #__slots__ = ()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        from abjad.tools import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        from abjad.tools import quantizationtools
        def recurse(node):
            result = []
            for child in node.children:
                if isinstance(child, quantizationtools.QGridLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            return result
        return tuple(recurse(self))

