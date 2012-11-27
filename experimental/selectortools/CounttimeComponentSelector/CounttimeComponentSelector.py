from abjad.tools import durationtools
from abjad.tools import iterationtools
from experimental import helpertools
from experimental.selectortools.TimeRelationSelector import TimeRelationSelector
from experimental.selectortools.SliceSelector import SliceSelector


class CounttimeComponentSelector(SliceSelector, TimeRelationSelector):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components restricted according to keywords.

        >>> from experimental import *

    Select the first five counttime components::

        >>> selectortools.CounttimeComponentSelector(stop_identifier=5)
        CounttimeComponentSelector(stop_identifier=5)

    Select the last five counttime components::

        >>> selectortools.CounttimeComponentSelector(start_identifier=-5)
        CounttimeComponentSelector(start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5``::

        >>> selectortools.CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)
        CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)

    Select all counttime components::

        >>> selectortools.CounttimeComponentSelector()
        CounttimeComponentSelector()

    Select counttime measure ``3`` to starting during segment ``'red'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = selectortools.SingleSegmentSelector(identifier='red')
        >>> time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.CounttimeComponentSelector(
        ... time_relation=time_relation, klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet_selector = selectortools.CounttimeComponentSelector(
        ... selector=measure_selector, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaf_slice_selector = selectortools.CounttimeComponentSelector(
        ... selector=tuplet_selector, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaf_slice_selector)
        selectortools.CounttimeComponentSelector(
            klass=leaftools.Leaf,
            selector=selectortools.CounttimeComponentSelector(
                klass=tuplettools.Tuplet,
                selector=selectortools.CounttimeComponentSelector(
                    time_relation=timerelationtools.TimespanTimespanTimeRelation(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4
                    ),
                start_identifier=-1
                ),
            start_identifier=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, klass=None, predicate=None, selector=None,
        start_identifier=None, stop_identifier=None, voice_name=None):
        from experimental import selectortools
        assert isinstance(selector, (selectortools.SliceSelector, type(None))), repr(selector)
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        SliceSelector.__init__(
            self, start_identifier=start_identifier, stop_identifier=stop_identifier, voice_name=voice_name)
        TimeRelationSelector.__init__(self, time_relation=time_relation)
        self._selector = selector
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def klass(self):
        '''Class of counttime component selector specified by user.

        Return counttime component class or none.
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

    ### PUBLIC METHODS ###

    # TODO: eventually merge with DivisionSelector.get_offsets() ... or maybe not
    def get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return pair.
        '''
        counttime_component_pairs = self.get_selected_objects(
            score_specification, voice_name, include_expression_start_offsets=True)
        #self._debug(counttime_component_pairs, 'counttime component pairs')
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
        for current_rhythm_region_expression in rhythm_region_expressions:
            if previous_rhythm_region_expression is not None:
                if not previous_rhythm_region_expression.stop_offset == \
                    current_rhythm_region_expression.start_offset:
                    return
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_expression.music, klass=self.klass):
                if self.time_relation is None or self.time_relation(
                    timespan_2=counttime_component,
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
