from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    '''A container in a ``QGrid`` structure:

    ::

        >>> container = quantizationtools.QGridContainer()

    ::

        >>> container
        QGridContainer(
            preprolated_duration=Duration(1, 1)
            )

    Used internally by ``QGrid``.

    Return ``QGridContainer`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    #__slots__ = ()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _leaf_klass(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QGridLeaf

    @property
    def _node_klass(self):
        from abjad.tools import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)
