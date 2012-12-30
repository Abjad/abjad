import copy
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools import helpertools
from experimental.tools.selectortools.Selector import Selector


class CounttimeComponentSelector(Selector):
    r'''Counttime component selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` leaves that start during score::

        >>> selector = score_specification.interface.select_leaves('Voice 1')

    ::
        
        >>> z(selector)
        selectortools.CounttimeComponentSelector(
            klass=leaftools.Leaf,
            voice_name='Voice 1'
            )

    Select voice ``1`` leaves that start during segment ``'red'``::

        >>> selector = red_segment.select_leaves('Voice 1')

    ::

        >>> z(selector)
        selectortools.CounttimeComponentSelector(
            anchor='red',
            klass=leaftools.Leaf,
            voice_name='Voice 1'
            )

    Counttime component selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, klass=None, predicate=None, 
        voice_name=None, time_relation=None,
        request_modifiers=None, timespan_modifiers=None):
        from experimental.tools import timeexpressiontools
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        Selector.__init__(self, 
            anchor=anchor, 
            voice_name=voice_name, time_relation=time_relation, 
            request_modifiers=request_modifiers,
            timespan_modifiers=timespan_modifiers)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate
    
    ### PRIVATE METHODS ###

    def _get_timespan(self, score_specification, voice_name):
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
        counttime_component_pairs = []
        previous_rhythm_region_expression = None
        timespan_1 = score_specification[self.anchor].timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation.set(timespan_1=timespan_1)
        for current_rhythm_region_expression in rhythm_region_expressions:
            if previous_rhythm_region_expression is not None:
                if not previous_rhtyhm_region_expression.stops_when_expr_starts(
                    current_rhythm_region_expression):
                    return selectiontools.Selection()
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_expression.music, klass=self.klass):
                if time_relation(timespan_2=counttime_component,
                    score_specification=score_specification,
                    context_name=voice_name):
                    counttime_component_pairs.append((
                        counttime_component, current_rhythm_region_expression.start_offset))
        counttime_component_pairs, dummy = self._apply_request_modifiers(counttime_component_pairs, None)
        first_component, first_component_expression_offset = counttime_component_pairs[0]
        last_component, last_component_expression_offset = counttime_component_pairs[-1]
        start_offset = first_component_expression_offset + first_component.start_offset
        stop_offset = last_component_expression_offset + last_component.stop_offset
        return timespantools.Timespan(start_offset, stop_offset)

    def _get_rhythm_region_expression(self, score_specification, voice_name,
        start_offset=None, stop_offset=None):
        from experimental.tools import settingtools
        assert voice_name == self.voice_name
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        rhythm_region_expressions = \
            score_specification.contexts[voice_name]['rhythm_region_expressions']
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        timespan_time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=anchor_timespan)
        rhythm_region_expressions = rhythm_region_expressions.get_timespans_that_satisfy_time_relation(
            timespan_time_relation)
        #self._debug(rhythm_region_expressions, 'rhythm region expressions')
        if not rhythm_region_expressions:
            return
        rhythm_region_expressions = copy.deepcopy(rhythm_region_expressions)
        rhythm_region_expressions = timespantools.TimespanInventory(rhythm_region_expressions)
        rhythm_region_expressions.sort()
        #self._debug_values(rhythm_region_expressions, 'rhythm region expressions')
        #self._debug(anchor_timespan, 'source timespan', blank=True)
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_region_expressions.keep_material_that_intersects_timespan(anchor_timespan)
        result = settingtools.OffsetPositionedRhythmExpression(
            voice_name=voice_name, start_offset=start_offset)
        for rhythm_region_expression in rhythm_region_expressions:
            result.music.extend(rhythm_region_expression.music)
        #self._debug(result, 'result')
        assert wellformednesstools.is_well_formed_component(result.music)
        #result, new_start_offset = counttime_component_selector._apply_request_modifiers(
        #    result, result.start_offset)
        result, new_start_offset = self._apply_request_modifiers(result, result.start_offset)
        result.set_offsets(start_offset=start_offset, stop_offset=stop_offset)
        result.repeat_to_stop_offset(stop_offset)
        return result

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
