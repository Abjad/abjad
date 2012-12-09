from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import timerelationtools
from experimental import helpertools
from experimental.symbolictimetools.TimeRelationSymbolicTimespan import TimeRelationSymbolicTimespan


class CounttimeComponentSymbolicTimespan(TimeRelationSymbolicTimespan):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components.

        >>> from experimental import *

    Select the first five counttime components::

        >>> symbolictimetools.CounttimeComponentSymbolicTimespan(stop_identifier=5)
        CounttimeComponentSymbolicTimespan(stop_identifier=5)

    Select the last five counttime components::

        >>> symbolictimetools.CounttimeComponentSymbolicTimespan(start_identifier=-5)
        CounttimeComponentSymbolicTimespan(start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5``::

        >>> symbolictimetools.CounttimeComponentSymbolicTimespan(start_identifier=5, stop_identifier=-5)
        CounttimeComponentSymbolicTimespan(start_identifier=5, stop_identifier=-5)

    Select all counttime components::

        >>> symbolictimetools.CounttimeComponentSymbolicTimespan()
        CounttimeComponentSymbolicTimespan()

    Select counttime measure ``3`` to starting during segment ``'red'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)

    ::

        >>> measure_selector = symbolictimetools.CounttimeComponentSymbolicTimespan(
        ... time_relation=time_relation, klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet_selector = symbolictimetools.CounttimeComponentSymbolicTimespan(
        ... selector=measure_selector, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaf_slice_selector = symbolictimetools.CounttimeComponentSymbolicTimespan(
        ... selector=tuplet_selector, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaf_slice_selector)
        symbolictimetools.CounttimeComponentSymbolicTimespan(
            klass=leaftools.Leaf,
            selector=symbolictimetools.CounttimeComponentSymbolicTimespan(
                klass=tuplettools.Tuplet,
                selector=symbolictimetools.CounttimeComponentSymbolicTimespan(
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4,
                    time_relation=timerelationtools.TimespanTimespanTimeRelation(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                            selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                                identifier='red'
                                )
                            )
                        )
                    ),
                start_identifier=-1
                ),
            start_identifier=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    # TODO: replace 'selector' with 'anchor'
    def __init__(self, anchor=None, klass=None, predicate=None, selector=None,
        start_identifier=None, stop_identifier=None, voice_name=None, time_relation=None):
        from experimental import symbolictimetools
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        TimeRelationSymbolicTimespan.__init__(self, 
            anchor=anchor, start_identifier=start_identifier, stop_identifier=stop_identifier, 
            voice_name=voice_name, time_relation=time_relation)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate
        self._selector = selector

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def klass(self):
        '''Class(es) of counttime component symbolic timespan.

        Return class, class inventory or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user.

        Return callback or none.
        '''
        return self._predicate

    @property
    def selector(self):
        '''Counttime component slice selector selector.

        To allow selectors to select recursively.

        Return slice selector.
        '''
        return self._selector

    # TODO: eventually remove in favor of TimeRelationSymbolicTimespan.start_segment_identifier
    @property
    def start_segment_identifier(self):
        return self.anchor

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, voice_name, start_segment_name=None):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return pair.
        '''
        counttime_component_pairs = self.get_selected_objects(
            score_specification, voice_name, include_expression_start_offsets=True)
        first_component, first_component_expression_offset = counttime_component_pairs[0]
        last_component, last_component_expression_offset = counttime_component_pairs[-1]
        start_offset = first_component_expression_offset + first_component.start_offset
        stop_offset = last_component_expression_offset + last_component.stop_offset
        return start_offset, stop_offset

    # TODO: eventually return selection
    def get_selected_objects(self, score_specification, voice_name, include_expression_start_offsets=False):
        '''Get counttime components selected when selector is applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return value of none means that selector can not yet interpret `score_specification`.

        Return list of object references or none.

        When ``include_expression_start_offsets=True`` return list of start offset / object pairs.

        .. note:: add examle with ``include_expression_start_offsets=True``.
        '''
        # allow user-specification selector voice name to override passed-in voice name
        voice_name = self.voice_name or voice_name
        rhythm_region_expressions = score_specification.contexts[voice_name]['rhythm_region_expressions']
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        if not rhythm_region_expressions:
            return
        if not rhythm_region_expressions[0].start_offset == durationtools.Offset(0):
            return
        counttime_components = []
        total_counttime_components = 0
        previous_rhythm_region_expression = None
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        timespan_1 = segment_specification.timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation
            time_relation._timespan_1 = timespan_1
        for current_rhythm_region_expression in rhythm_region_expressions:
            if previous_rhythm_region_expression is not None:
                if not previous_rhythm_region_expression.stop_offset == \
                    current_rhythm_region_expression.start_offset:
                    return
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_expression.music, klass=self.klass):
                if time_relation(timespan_2=counttime_component,
                    score_specification=score_specification,
                    context_name=voice_name):
                    if include_expression_start_offsets:
                        counttime_components.append((
                            counttime_component, current_rhythm_region_expression.start_offset))
                    else:
                        counttime_components.append(counttime_component)
                    total_counttime_components += 1
                    if total_counttime_components == self.stop_identifier:
                        break
            if total_counttime_components == self.stop_identifier:
                break
        counttime_components = counttime_components[self.start_identifier:self.stop_identifier]
        return counttime_components
