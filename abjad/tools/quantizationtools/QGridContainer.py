from abjad.tools.rhythmtreetools.RhythmTreeContainer import RhythmTreeContainer


class QGridContainer(RhythmTreeContainer):
    r'''Q-grid container.

    ..  container:: example

        >>> container = abjad.quantizationtools.QGridContainer()
        >>> abjad.f(container)
        abjad.quantizationtools.QGridContainer(
            preprolated_duration=abjad.Duration(1, 1),
            )

    Used internally by ``QGrid``.
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
