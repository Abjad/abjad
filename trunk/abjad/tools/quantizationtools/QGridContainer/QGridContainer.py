# -*- encoding: utf-8 -*-
from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    r'''A container in a ``QGrid`` structure:

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

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QGridLeaf

    @property
    def _node_class(self):
        from abjad.tools import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)
