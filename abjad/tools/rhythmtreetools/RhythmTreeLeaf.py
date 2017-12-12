from abjad.tools import graphtools
from abjad.tools import scoretools
from abjad.tools.datastructuretools.TreeNode import TreeNode
from abjad.tools.rhythmtreetools.RhythmTreeMixin import RhythmTreeMixin


class RhythmTreeLeaf(RhythmTreeMixin, TreeNode):
    r'''Rhythm-tree leaf.

    ..  container:: example

        >>> leaf = abjad.rhythmtreetools.RhythmTreeLeaf(
        ...     preprolated_duration=5, is_pitched=True)
        >>> leaf
        RhythmTreeLeaf(
            preprolated_duration=Duration(5, 1),
            is_pitched=True
            )

    ..  container:: example

        Calls with a pulse preprolated duration to generate leaves:

        >>> result = leaf((1, 8))
        >>> result
        Selection([Note("c'2"), Note("c'8")])

    ..  container:: example

        Generates rests when called if `is_pitched` is false:

        >>> abjad.rhythmtreetools.RhythmTreeLeaf(
        ...     preprolated_duration=7, is_pitched=False)((1, 16))
        Selection([Rest('r4..')])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_is_pitched',
        '_offset',
        '_offsets_are_current',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        preprolated_duration=1,
        is_pitched=True,
        name=None,
        ):
        TreeNode.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        self.is_pitched = is_pitched

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        r'''Generate Abjad score components:

        >>> leaf = abjad.rhythmtreetools.RhythmTreeLeaf(5)
        >>> leaf((1, 4))
        Selection([Note("c'1"), Note("c'4")])

        Returns sequence of components.
        '''
        import abjad
        pulse_duration = abjad.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        maker = abjad.LeafMaker()
        if self.is_pitched:
            return maker(0, total_duration)
        return maker([None], total_duration)

    def __graph__(self, **keywords):
        r'''Graphviz graph of rhythm tree leaf.
        '''
        graph = graphtools.GraphvizGraph(name='G')
        node = graphtools.GraphvizNode(
            attributes={
                'label': str(self.preprolated_duration),
                'shape': 'box'
                }
            )
        graph.append(node)
        return graph

    ### PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.preprolated_duration)]

    ### PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        r'''RTM format of rhythm tree leaf.

        >>> abjad.rhythmtreetools.RhythmTreeLeaf(1, is_pitched=True).rtm_format
        '1'
        >>> abjad.rhythmtreetools.RhythmTreeLeaf(5, is_pitched=False).rtm_format
        '-5'

        Returns string.
        '''
        if self.is_pitched:
            return '{!s}'.format(self.preprolated_duration)
        return '-{!s}'.format(self.preprolated_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def is_pitched(self):
        r'''Gets and sets boolean equal to  true if leaf is pitched.
        Otherwise false.

        >>> leaf = abjad.rhythmtreetools.RhythmTreeLeaf()
        >>> leaf.is_pitched
        True

        >>> leaf.is_pitched = False
        >>> leaf.is_pitched
        False

        Returns true or false.
        '''
        return self._is_pitched

    @is_pitched.setter
    def is_pitched(self, argument):
        self._is_pitched = bool(argument)
