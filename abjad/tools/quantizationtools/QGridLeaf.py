# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad.tools.datastructuretools import TreeNode
from abjad.tools.rhythmtreetools import RhythmTreeMixin


class QGridLeaf(RhythmTreeMixin, TreeNode):
    r'''A leaf in a ``QGrid`` structure.

    ::

        >>> leaf = quantizationtools.QGridLeaf()

    ::

        >>> leaf
        QGridLeaf(
            preprolated_duration=Duration(1, 1),
            is_divisible=True
            )

    Used internally by ``QGrid``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_is_divisible',
        '_offset',
        '_offsets_are_current',
        '_q_event_proxies',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        preprolated_duration=1,
        q_event_proxies=None,
        is_divisible=True,
        ):
        from abjad.tools import quantizationtools
        TreeNode.__init__(self)
        RhythmTreeMixin.__init__(self, preprolated_duration)
        if q_event_proxies is None:
            self._q_event_proxies = []
        else:
            assert all(isinstance(x, quantizationtools.QEventProxy)
                for x in q_event_proxies)
            self._q_event_proxies = list(q_event_proxies)
        self._is_divisible = bool(is_divisible)

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        r'''Calls q-grid leaf.

        Returns selection of notes.
        '''
        pulse_duration = durationtools.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        return scoretools.make_notes(0, total_duration)

    def __graph__(self, **kwargs):
        r'''Graphviz graph of q-grid leaf.

        Returns Graphviz graph.
        '''
        from abjad.tools import documentationtools
        graph = documentationtools.GraphvizGraph(name='G')
        node = documentationtools.GraphvizNode(
            attributes={
                'label': str(self.preprolated_duration),
                'shape': 'box'
                }
            )
        graph.append(node)
        return graph

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_names
        template_names = names[:]
        if 'q_event_proxies' in names and not self.q_event_proxies:
            names.remove('q_event_proxies')
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_kwargs_names=names,
            template_names=template_names,
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.preprolated_duration)]

    ### PUBLIC PROPERTIES ###

    @property
    def is_divisible(self):
        r'''Flag for whether the node may be further divided
        under some search tree.
        '''
        return self._is_divisible

    @is_divisible.setter
    def is_divisible(self, arg):
        self._is_divisible = bool(arg)

    @property
    def preceding_q_event_proxies(self):
        r'''Preceding q-event proxies of q-grid leaf.

        Returns list.
        '''
        return [x for x in self._q_event_proxies
            if x.offset < self.start_offset]

    @property
    def q_event_proxies(self):
        r'''Q-event proxies of q-grid leaf.
        '''
        return self._q_event_proxies

    @property
    def rtm_format(self):
        r'''RTM format of q-grid leaf.
        '''
        return str(self.preprolated_duration)

    @property
    def succeeding_q_event_proxies(self):
        r'''Succeeding q-event proxies of q-grid leaf.

        Returns list.
        '''
        return [x for x in self._q_event_proxies
            if self.start_offset <= x.offset]
