from abjad.tools.quantizationtools.QGridLeaf import QGridLeaf
from abjad.tools.rhythmtreetools.RhythmTreeContainer import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    r'''Q-grid container.

    ..  container:: example

        >>> container = abjad.quantizationtools.QGridContainer()
        >>> abjad.f(container)
        abjad.quantizationtools.QGridContainer(
            children=(),
            preprolated_duration=abjad.Duration(1, 1),
            )

    Used internally by ``QGrid``.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def leaves(self):
        '''
        Get leaves.
        '''
        return tuple(
            _ for _ in self.depth_first()
            if isinstance(_, QGridLeaf)
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        from abjad.tools import quantizationtools
        return quantizationtools.QGridLeaf

    @property
    def _node_class(self):
        from abjad.tools import quantizationtools
        return (type(self), quantizationtools.QGridLeaf)
