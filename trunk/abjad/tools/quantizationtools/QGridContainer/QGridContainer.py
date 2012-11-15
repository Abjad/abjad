from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    '''A container in a ``QGrid`` structure:

    ::

        >>> container = quantizationtools.QGridContainer()

    ::

        >>> container
        quantizationtools.QGridContainer(
            duration=durationtools.Duration(1, 1),
            children=()
            )

    Used internally by ``QGrid``.

    Return ``QGridContainer`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()


    ### SPECIAL METHODS ###
    
    def __repr__(self):
        return self._tools_package_qualified_indented_repr

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

