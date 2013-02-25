from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools.rhythmtreetools.RhythmTreeNode import RhythmTreeNode


class RhythmTreeLeaf(RhythmTreeNode):
    '''A leaf node in a rhythm tree:

    ::

        >>> leaf = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=5, is_pitched=True)
        >>> leaf
        RhythmTreeLeaf(
            preprolated_duration=Duration(5, 1),
            is_pitched=True
            )

    Call with a pulse preprolated_duration to generate Abjad leaf objects:

    ::

        >>> result = leaf((1, 8))
        >>> result
        [Note("c'2"), Note("c'8")]

    Generates rests when called, if `is_pitched` is False:

    ::

        >>> rhythmtreetools.RhythmTreeLeaf(preprolated_duration=7, is_pitched=False)((1, 16))
        [Rest('r4..')]

    Return `RhythmTreeLeaf`.
    '''

    ### INITIALIZER ###

    def __init__(self, preprolated_duration=1, is_pitched=True, name=None):
        RhythmTreeNode.__init__(self, preprolated_duration=preprolated_duration, name=name)
        self.is_pitched = is_pitched

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        '''Generate Abjad score components:

        ::

            >>> leaf = rhythmtreetools.RhythmTreeLeaf(5)
            >>> leaf((1, 4))
            [Note("c'1"), Note("c'4")]

        Return sequence of components.
        '''
        pulse_duration = durationtools.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        if self.is_pitched:
            return notetools.make_notes(0, total_duration)
        return resttools.make_rests(total_duration)

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self.preprolated_duration == expr.preprolated_duration:
                if self.is_pitched == expr.is_pitched:
                    return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.preprolated_duration)]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def graphviz_graph(self):
        graph = documentationtools.GraphvizGraph(name='G')
        node = documentationtools.GraphvizNode(
            attributes={
                label: str(self.preprolated_duration),
                shape: 'box'
            }
            )
        graph.append(node)
        return graph

    @property
    def rtm_format(self):
        '''The node's RTM format:

        ::

            >>> rhythmtreetools.RhythmTreeLeaf(1, is_pitched=True).rtm_format
            '1'
            >>> rhythmtreetools.RhythmTreeLeaf(5, is_pitched=False).rtm_format
            '-5'

        Return string.
        '''
        if self.is_pitched:
            return '{}'.format(self.preprolated_duration)
        return '-{}'.format(self.preprolated_duration)

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def is_pitched():
        def fget(self):
            '''True if leaf is pitched:

            ::

                >>> leaf = rhythmtreetools.RhythmTreeLeaf()
                >>> leaf.is_pitched
                True

            ::

                >>> leaf.is_pitched = False
                >>> leaf.is_pitched
                False

            Return boolean.
            '''
            return self._is_pitched
        def fset(self, arg):
            self._is_pitched = bool(arg)
        return property(**locals())

