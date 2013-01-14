import copy
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import tuplettools
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
            classes=selectortools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Select voice ``1`` leaves that start during segment ``'red'``::

        >>> selector = red_segment.select_leaves('Voice 1')

    ::

        >>> z(selector)
        selectortools.CounttimeComponentSelector(
            anchor='red',
            classes=selectortools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Counttime component selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, classes=None, 
        voice_name=None, time_relation=None, payload_callbacks=None, timespan_callbacks=None):
        from experimental.tools import selectortools
        from experimental.tools import settingtools
        assert classes is None or self._is_counttime_component_class_expr(classes), repr(classes)
        Selector.__init__(self, 
            anchor=anchor, 
            voice_name=voice_name, 
            time_relation=time_relation, 
            payload_callbacks=payload_callbacks,
            timespan_callbacks=timespan_callbacks)
        if isinstance(classes, tuple):
            classes = selectortools.ClassInventory(classes)
        self._classes = classes
    
    ### PRIVATE METHODS ###

    # TODO: remove start_offset=None, stop_offset=None keywords and use payload callback instead.
    # TODO: migrate into self._get_timespan_and_payload().
    def _get_payload(self, score_specification, voice_name, start_offset=None, stop_offset=None):
        from experimental.tools import settingtools
        assert voice_name == self.voice_name
        assert start_offset is not None, repr(start_offset)
        assert stop_offset is not None, repr(stop_offset)
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        voice_proxy = score_specification.contexts[voice_name]
        rhythm_region_products = voice_proxy.rhythm_region_products
        time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        rhythm_region_products = rhythm_region_products.get_timespans_that_satisfy_time_relation(time_relation)
        if not rhythm_region_products:
            return
        rhythm_region_products = copy.deepcopy(rhythm_region_products)
        rhythm_region_products = timespantools.TimespanInventory(rhythm_region_products)
        rhythm_region_products.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_region_products = rhythm_region_products & anchor_timespan
        timespan = timespantools.Timespan(start_offset)
        result = settingtools.RhythmRegionProduct(voice_name=voice_name, timespan=timespan)
        for rhythm_region_product in rhythm_region_products:
            result.payload.extend(rhythm_region_product.payload)
        assert wellformednesstools.is_well_formed_component(result.payload)
        result, new_start_offset = self._apply_payload_callbacks(result, result.start_offset)
        assert isinstance(result, settingtools.RhythmRegionProduct), repr(result)
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        assert not keep_timespan.starts_before_timespan_starts(result.timespan), repr((result.timespan, keep_timespan))
        assert result.timespan.start_offset == keep_timespan.start_offset, repr((result.timespan, keep_timespan))
        result = result & keep_timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1
        result = result[0]
        assert isinstance(result, settingtools.RhythmRegionProduct), repr(result)
        result.repeat_to_stop_offset(stop_offset)
        return result

    # TODO: migrate into self._get_timespan_and_payload()
    def _get_timespan(self, score_specification, voice_name):
        # allow user-specified voice name to override passed-in voice name
        voice_name = self.voice_name or voice_name
        rhythm_region_products = score_specification.contexts[voice_name].rhythm_region_products
        if not rhythm_region_products:
            return selectiontools.Selection()
        if not rhythm_region_products[0].start_offset == durationtools.Offset(0):
            return selectiontools.Selection()
        counttime_component_pairs = []
        previous_rhythm_region_product = None
        timespan_1 = score_specification[self.anchor].timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation.new(timespan_1=timespan_1)
        for current_rhythm_region_product in rhythm_region_products:
            if previous_rhythm_region_product is not None:
                if not previous_rhtyhm_region_product.stops_when_expr_starts(
                    current_rhythm_region_product):
                    return selectiontools.Selection()
            for counttime_component in iterationtools.iterate_components_in_expr(
                current_rhythm_region_product.payload, klass=tuple(self.classes)):
                if time_relation(timespan_2=counttime_component,
                    score_specification=score_specification,
                    context_name=voice_name):
                    counttime_component_pairs.append((
                        counttime_component, current_rhythm_region_product.start_offset))
        counttime_component_pairs, dummy = self._apply_payload_callbacks(counttime_component_pairs, None)
        first_component, first_component_expression_offset = counttime_component_pairs[0]
        last_component, last_component_expression_offset = counttime_component_pairs[-1]
        start_offset = first_component_expression_offset + first_component.start_offset
        stop_offset = last_component_expression_offset + last_component.stop_offset
        return timespantools.Timespan(start_offset, stop_offset)

    # TODO: eventually collapse self._get_payload() and self._get_timespan() into this method
    def _get_timespan_and_payload(self, score_specification, voice_name):
        raise NotImplementedError

    def _is_counttime_component_class_expr(self, expr):
        from experimental.tools import helpertools
        from experimental.tools import selectortools
        if isinstance(expr, tuple) and all([self._is_counttime_component_class_expr(x) for x in expr]):
            return True
        elif isinstance(expr, selectortools.ClassInventory):
            return True
        elif issubclass(expr, (measuretools.Measure, tuplettools.Tuplet, leaftools.Leaf)):
            return True
        elif expr == containertools.Container:
            return True
        else:
            return False

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def classes(self):
        '''Classes of counttime component selector.

        Return class inventory or none.
        '''
        return self._classes
