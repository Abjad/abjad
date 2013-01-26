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
from experimental.tools.settingtools.SelectExpression import SelectExpression


class CounttimeComponentSelectExpression(SelectExpression):
    r'''Counttime component select expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` leaves that start during score::

        >>> select_expression = score_specification.interface.select_leaves('Voice 1')

    ::
        
        >>> z(select_expression)
        settingtools.CounttimeComponentSelectExpression(
            classes=settingtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Select voice ``1`` leaves that start during segment ``'red'``::

        >>> select_expression = red_segment.select_leaves('Voice 1')

    ::

        >>> z(select_expression)
        settingtools.CounttimeComponentSelectExpression(
            anchor='red',
            classes=settingtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Counttime component select expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, anchor=None, classes=None, voice_name=None, time_relation=None, callbacks=None):
        from experimental.tools import settingtools
        assert classes is None or self._is_counttime_component_class_expr(classes), repr(classes)
        SelectExpression.__init__(self, 
            anchor=anchor, 
            voice_name=voice_name, 
            time_relation=time_relation, 
            callbacks=callbacks)
        if isinstance(classes, tuple):
            classes = settingtools.ClassInventory(classes)
        self._classes = classes
    
    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        anchor_timespan = self.get_anchor_timespan()
        voice_proxy = self.score_specification.contexts[self.voice_name]
        rhythm_payload_expressions = voice_proxy.rhythm_payload_expressions
        time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        rhythm_payload_expressions = rhythm_payload_expressions.get_timespans_that_satisfy_time_relation(time_relation)
        if not rhythm_payload_expressions:
            return
        rhythm_payload_expressions = copy.deepcopy(rhythm_payload_expressions)
        rhythm_payload_expressions = timespantools.TimespanInventory(rhythm_payload_expressions)
        rhythm_payload_expressions.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_payload_expressions &= anchor_timespan
        expression = settingtools.StartPositionedRhythmPayloadExpression(start_offset=anchor_timespan.start_offset)
        for rhythm_payload_expression in rhythm_payload_expressions:
            expression.payload.extend(rhythm_payload_expression.payload)
        assert wellformednesstools.is_well_formed_component(expression.payload)
        expression = self._apply_callbacks(expression)
        expression._voice_name = self.voice_name
        return expression

    def _is_counttime_component_class_expr(self, expr):
        from experimental.tools import settingtools
        if isinstance(expr, tuple) and all([self._is_counttime_component_class_expr(x) for x in expr]):
            return True
        elif isinstance(expr, settingtools.ClassInventory):
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
        '''Classes of counttime component select expression.

        Return class inventory or none.
        '''
        return self._classes
