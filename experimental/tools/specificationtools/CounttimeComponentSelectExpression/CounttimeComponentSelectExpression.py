import copy
from abjad.tools import componenttools
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import leaftools
from abjad.tools import measuretools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import tuplettools
from abjad.tools import wellformednesstools
from experimental.tools.specificationtools.CounttimeComponentSelectExpressionSetMethodMixin import \
    CounttimeComponentSelectExpressionSetMethodMixin
from experimental.tools.specificationtools.SelectExpression import SelectExpression


class CounttimeComponentSelectExpression(CounttimeComponentSelectExpressionSetMethodMixin, SelectExpression):
    r'''Counttime component select expression.

    Preparatory definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example 1. Select voice ``1`` leaves that start during score:

    ::

        >>> select_expression = score_specification.select_leaves('Voice 1')

    ::

        >>> z(select_expression)
        specificationtools.CounttimeComponentSelectExpression(
            classes=specificationtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Example 2. Select voice ``1`` leaves that start during segment ``'red'``:

    ::

        >>> select_expression = red_segment.select_leaves('Voice 1')

    ::

        >>> z(select_expression)
        specificationtools.CounttimeComponentSelectExpression(
            anchor='red',
            classes=specificationtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Counttime component select expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, classes=None, voice_name=None, time_relation=None, callbacks=None):
        from experimental.tools import specificationtools
        assert classes is None or self._is_counttime_component_class_expr(classes), repr(classes)
        SelectExpression.__init__(self,
            anchor=anchor,
            voice_name=voice_name,
            time_relation=time_relation,
            callbacks=callbacks)
        CounttimeComponentSelectExpressionSetMethodMixin.__init__(self)
        if isinstance(classes, tuple):
            classes = specificationtools.ClassInventory(classes)
        self._classes = classes

    ### SPECIAL METHODS ###

    def __add__(self, select_expression):
        from experimental.tools import specificationtools
        assert isinstance(select_expression, type(self)), repr(select_expression)
        assert self.score_specification is select_expression.score_specification
        select_expression_inventory = specificationtools.SelectExpressionInventory()
        select_expression_inventory.extend([copy.deepcopy(self), copy.deepcopy(select_expression)])
        select_expression_inventory._score_specification = self.score_specification
        return select_expression_inventory

    ### PRIVATE METHODS ###

    def _is_counttime_component_class_expr(self, expr):
        from experimental.tools import specificationtools
        if isinstance(expr, tuple) and all([self._is_counttime_component_class_expr(x) for x in expr]):
            return True
        elif isinstance(expr, specificationtools.ClassInventory):
            return True
        elif issubclass(expr, (measuretools.Measure, tuplettools.Tuplet, leaftools.Leaf)):
            return True
        elif expr == containertools.Container:
            return True
        else:
            return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def classes(self):
        '''Counttime component select expression classes.

        Return class inventory or none.
        '''
        return self._classes

    ### PUBLIC METHODS ###

    def evaluate(self):
        '''Evaluate counttime component select expression.

        Return none when nonevaluable.

        Return start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import specificationtools
        anchor_timespan = self._evaluate_anchor_timespan()
        voice_proxy = self.score_specification.voice_data_structures_by_voice[self.voice_name]
        rhythm_payload_expressions = voice_proxy.payload_expressions_by_attribute['rhythm']
        rhythm_payload_expressions = rhythm_payload_expressions.get_timespans_that_satisfy_time_relation(
            timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan))
        if not rhythm_payload_expressions:
            return
        rhythm_payload_expressions = copy.deepcopy(rhythm_payload_expressions)
        rhythm_payload_expressions = timespantools.TimespanInventory(rhythm_payload_expressions)
        rhythm_payload_expressions.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_payload_expressions &= anchor_timespan
        expression = specificationtools.StartPositionedRhythmPayloadExpression(
            start_offset=anchor_timespan.start_offset)
        for rhythm_payload_expression in rhythm_payload_expressions:
            expression.payload.extend(rhythm_payload_expression.payload)
        assert wellformednesstools.is_well_formed_component(expression.payload)
        # TODO: eventually make this be able to work
        #expression = expression.get_elements_that_satisfy_time_relation(time_relation)
        expression = self._apply_callbacks(expression)
        expression._voice_name = self.voice_name
        return expression

    def evaluate_against_score(self, score):
        '''Evaluate counttime component select expression against `score`.

        Return iterable payload expression.
        '''
        from experimental.tools import specificationtools
        assert isinstance(score, scoretools.Score), repr(score)
        voice = score[self.voice_name]
        anchor_timespan = self._evaluate_anchor_timespan()
        # list signals the result of a call to map_to_each()
        if isinstance(anchor_timespan, list):
            is_map_to_each = True
        else:
            is_map_to_each = False
            anchor_timespan = [anchor_timespan]
        result = []
        anchor_timespans = anchor_timespan
        for anchor_timespan in anchor_timespans:
            time_relation = self._get_time_relation(anchor_timespan)
            components = list(iterationtools.iterate_components_in_expr(voice, klass=tuple(self.classes)))
            components = timerelationtools.get_counttime_components_that_satisfy_time_relation(
                components, time_relation)
            #voice_proxy = self.score_specification.voice_data_structures_by_voice[self.voice_name]
            #start, stop = timerelationtools.get_offset_indices_that_satisfy_time_relation(
            #    voice_proxy.leaf_start_offsets, voice_proxy.leaf_stop_offsets, time_relation)
            #print start, stop
            #components = voice_proxy.leaves[start:stop]
            if not components:
                continue
            expression = specificationtools.IterablePayloadExpression(components)
            expression = self._apply_callbacks(expression)
            result.append(expression)
        if is_map_to_each:
            return result
        else:
            expression = result[0]
            return expression
