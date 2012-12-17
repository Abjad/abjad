from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools import helpertools
from experimental.tools.symbolictimetools.VoiceSelector import VoiceSelector


class CounttimeComponentSelector(VoiceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

    Select the first five counttime components::

        >>> symbolictimetools.CounttimeComponentSelector(stop_identifier=5)
        CounttimeComponentSelector(stop_identifier=5)

    Select the last five counttime components::

        >>> symbolictimetools.CounttimeComponentSelector(start_identifier=-5)
        CounttimeComponentSelector(start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5``::

        >>> symbolictimetools.CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)
        CounttimeComponentSelector(start_identifier=5, stop_identifier=-5)

    Select all counttime components::

        >>> symbolictimetools.CounttimeComponentSelector()
        CounttimeComponentSelector()

    Select counttime measure ``3`` to starting during segment ``'red'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> measures = symbolictimetools.CounttimeComponentSelector(
        ... anchor='red', klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet = symbolictimetools.CounttimeComponentSelector(
        ... anchor=measures, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaves = symbolictimetools.CounttimeComponentSelector(
        ... anchor=tuplet, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaves)
        symbolictimetools.CounttimeComponentSelector(
            anchor=symbolictimetools.CounttimeComponentSelector(
                anchor=symbolictimetools.CounttimeComponentSelector(
                    anchor='red',
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4
                    ),
                klass=tuplettools.Tuplet,
                start_identifier=-1
                ),
            klass=leaftools.Leaf,
            start_identifier=-3
            )

    Counttime component symbolic timespans are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, klass=None, predicate=None, 
        start_identifier=None, stop_identifier=None, voice_name=None, time_relation=None,
        timespan_modifications=None, selector_modifications=None):
        from experimental.tools import symbolictimetools
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        VoiceSelector.__init__(self, 
            anchor=anchor, start_identifier=start_identifier, stop_identifier=stop_identifier, 
            voice_name=voice_name, time_relation=time_relation, 
            timespan_modifications=timespan_modifications, selector_modifications=selector_modifications)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate
    
    ### SPECIAL METHODS ###

    # TODO: streamline with __getnewargs__ or equivalent
    def __deepcopy__(self, memo):
        result = type(self)(
            anchor=self.anchor, klass=self.klass, predicate=self.predicate,
            start_identifier=self.start_identifier, stop_identifier=self.stop_identifier, 
            voice_name=self.voice_name, time_relation=self.time_relation, 
            timespan_modifications=self.timespan_modifications, 
            selector_modifications=self.selector_modifications)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of symbolic timespan when applied
        to `voice_name` in `score_specification`.

        Return offset pair.
        '''
        # allow user-specified voice name to override passed-in voice name
        voice_name = self.voice_name or voice_name
        rhythm_region_expressions = score_specification.contexts[voice_name]['rhythm_region_expressions']
        if not rhythm_region_expressions:
            return selectiontools.Selection()
        if not rhythm_region_expressions[0].start_offset == durationtools.Offset(0):
            return selectiontools.Selection()
        counttime_components = []
        total_counttime_components = 0
        previous_rhythm_region_expression = None
        start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(self.anchor)
        timespan_1 = timespantools.Timespan(start_offset, stop_offset)
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation
            time_relation._timespan_1 = timespan_1
        for current_rhythm_region_expression in rhythm_region_expressions:
            if previous_rhythm_region_expression is not None:
                if not previous_rhythm_region_expression.stop_offset == \
                    current_rhythm_region_expression.start_offset:
                    return selectiontools.Selection()
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_expression.music, klass=self.klass):
                if time_relation(timespan_2=counttime_component,
                    score_specification=score_specification,
                    context_name=voice_name):
                    counttime_components.append((
                        counttime_component, current_rhythm_region_expression.start_offset))
                    total_counttime_components += 1
                    if total_counttime_components == self.stop_identifier:
                        break
            if total_counttime_components == self.stop_identifier:
                break
        counttime_components = counttime_components[self.start_identifier:self.stop_identifier]
        counttime_component_pairs = counttime_components
        first_component, first_component_expression_offset = counttime_component_pairs[0]
        last_component, last_component_expression_offset = counttime_component_pairs[-1]
        start_offset = first_component_expression_offset + first_component.start_offset
        stop_offset = last_component_expression_offset + last_component.stop_offset
        return start_offset, stop_offset

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def klass(self):
        '''Class(es) of counttime component symbolic timespan.

        Return class, class inventory or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component symbolic timespan specified by user.

        Return predicate or none.
        '''
        return self._predicate
