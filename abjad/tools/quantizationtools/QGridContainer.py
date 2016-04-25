# -*- coding: utf-8 -*-
from abjad.tools.rhythmtreetools import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    r'''A container in a ``QGrid`` structure:

    ::

        >>> container = quantizationtools.QGridContainer()

    ::

        >>> print(format(container))
        quantizationtools.QGridContainer(
            preprolated_duration=durationtools.Duration(1, 1),
            )

    Used internally by ``QGrid``.

    Return ``QGridContainer`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QGridLeaf

    @property
    def _node_class(self):
        from abjad.tools import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)
