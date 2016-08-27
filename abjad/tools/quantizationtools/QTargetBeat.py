# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class QTargetBeat(AbjadObject):
    r'''Representation of a single "beat" in a quantization target.

    ::

        >>> beatspan = (1, 8)
        >>> offset_in_ms = 1500
        >>> search_tree = quantizationtools.UnweightedSearchTree({3: None})
        >>> tempo = Tempo((1, 4), 56)

    ::

        >>> q_target_beat = quantizationtools.QTargetBeat(
        ...     beatspan=beatspan,
        ...     offset_in_ms=offset_in_ms,
        ...     search_tree=search_tree,
        ...     tempo=tempo,
        ...     )

    ::

        >>> print(format(q_target_beat))
        quantizationtools.QTargetBeat(
            beatspan=durationtools.Duration(1, 8),
            offset_in_ms=durationtools.Offset(1500, 1),
            search_tree=quantizationtools.UnweightedSearchTree(
                definition={   3: None,
                    },
                ),
            tempo=indicatortools.Tempo(
                reference_duration=durationtools.Duration(1, 4), 
                units_per_minute=56,
                ),
            )

    Not composer-safe.

    Used internally by ``Quantizer``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beatspan',
        '_distances',
        '_grouping',
        '_offset_in_ms',
        '_q_events',
        '_q_grid',
        '_q_grids',
        '_search_tree',
        '_tempo',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beatspan=None,
        offset_in_ms=None,
        search_tree=None,
        tempo=None,
        ):
        from abjad.tools import quantizationtools

        beatspan = beatspan or durationtools.Duration(0)
        beatspan = durationtools.Duration(beatspan)
        offset_in_ms = offset_in_ms or durationtools.Duration(0)
        offset_in_ms = durationtools.Offset(offset_in_ms)

        if search_tree is None:
            search_tree = quantizationtools.UnweightedSearchTree()
        assert isinstance(search_tree, quantizationtools.SearchTree)
        tempo = tempo or indicatortools.Tempo(durationtools.Duration(1, 4), 60)
        #tempo = indicatortools.Tempo(tempo)
        if isinstance(tempo, tuple):
            tempo = indicatortools.Tempo(*tempo)
        assert not tempo.is_imprecise

        q_events = []
        q_grids = []

        self._beatspan = beatspan
        self._distances = {}
        self._offset_in_ms = offset_in_ms
        self._q_events = q_events
        self._q_grid = None
        self._q_grids = q_grids
        self._search_tree = search_tree
        self._tempo = tempo

    ### SPECIAL METHODS ###

    def __call__(self, job_id):
        r'''Calls q-target beat.

        Returns quantization job.
        '''
        from abjad.tools import quantizationtools
        if not self.q_events:
            return None
        assert all(isinstance(x, quantizationtools.QEvent)
            for x in self.q_events)
        q_event_proxies = []
        for q_event in self.q_events:
            q_event_proxy = quantizationtools.QEventProxy(
                q_event,
                self.offset_in_ms,
                self.offset_in_ms + self.duration_in_ms,
                )
            q_event_proxies.append(q_event_proxy)
        return quantizationtools.QuantizationJob(
            job_id, self.search_tree, q_event_proxies)

    def __format__(self, format_specification=''):
        r'''Formats q-event.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def beatspan(self):
        r'''Beatspan of q-target beat.

        ::

            >>> q_target_beat.beatspan
            Duration(1, 8)

        Returns duration.
        '''
        return self._beatspan

    @property
    def distances(self):
        r'''A list of computed distances between the ``QEventProxies``
        associated with a ``QTargetBeat`` instance, and each ``QGrid``
        generated for that beat.

        Used internally by the ``Quantizer``.

        Returns tuple.
        '''
        return self._distances

    @property
    def duration_in_ms(self):
        r'''Duration in milliseconds of the q-targeg beat.

        ::

            >>> q_target_beat.duration_in_ms
            Duration(3750, 7)

        Returns duration.
        '''
        from abjad.tools import quantizationtools
        return self.tempo.duration_to_milliseconds(self.beatspan)

    @property
    def offset_in_ms(self):
        r'''Offset in milliseconds of q-target beat.

        ::

            >>> q_target_beat.offset_in_ms
            Offset(1500, 1)

        Returns offset.
        '''
        return self._offset_in_ms

    @property
    def q_events(self):
        r'''A list for storing ``QEventProxy`` instances.

        Used internally by the ``Quantizer``.

        Returns list.
        '''
        return self._q_events

    @property
    def q_grid(self):
        r'''The ``QGrid`` instance selected by a ``Heuristic``.

        Used internally by the ``Quantizer``.

        Returns ``QGrid`` instance.
        '''
        return self._q_grid

    @property
    def q_grids(self):
        r'''A tuple of ``QGrids`` generated by a ``QuantizationJob``.

        Used internally by the ``Quantizer``.

        Returns tuple.
        '''
        return self._q_grids

    @property
    def search_tree(self):
        r'''Search tree of q-target beat.

        ::

            >>> q_target_beat.search_tree
            UnweightedSearchTree(definition={3: None})

        Returns search tree.
        '''
        return self._search_tree

    @property
    def tempo(self):
        r'''Tempo of q-target beat.

        ::

            >>> q_target_beat.tempo
            Tempo(reference_duration=Duration(1, 4), units_per_minute=56)

        Returns tempo.
        '''
        return self._tempo
