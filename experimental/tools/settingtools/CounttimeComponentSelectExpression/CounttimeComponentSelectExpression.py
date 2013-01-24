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
    r'''Counttime component selector.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` leaves that start during score::

        >>> selector = score_specification.interface.select_leaves('Voice 1')

    ::
        
        >>> z(selector)
        settingtools.CounttimeComponentSelectExpression(
            classes=settingtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Select voice ``1`` leaves that start during segment ``'red'``::

        >>> selector = red_segment.select_leaves('Voice 1')

    ::

        >>> z(selector)
        settingtools.CounttimeComponentSelectExpression(
            anchor='red',
            classes=settingtools.ClassInventory([
                leaftools.Leaf
                ]),
            voice_name='Voice 1'
            )

    Counttime component selectors are immutable.
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
        rhythm_products = voice_proxy.rhythm_products
        time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        rhythm_products = rhythm_products.get_timespans_that_satisfy_time_relation(time_relation)
        if not rhythm_products:
            return
        rhythm_products = copy.deepcopy(rhythm_products)
        rhythm_products = timespantools.TimespanInventory(rhythm_products)
        rhythm_products.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_products &= anchor_timespan
        result = settingtools.VoicedStartPositionedRhythmPayloadExpression(
            voice_name=self.voice_name, start_offset=anchor_timespan.start_offset)
        for rhythm_product in rhythm_products:
            result.payload.extend(rhythm_product.payload)
        assert wellformednesstools.is_well_formed_component(result.payload)
        result = self._apply_callbacks(result)
        assert isinstance(result, settingtools.VoicedStartPositionedRhythmPayloadExpression), repr(result)
        return result

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
        '''Classes of counttime component selector.

        Return class inventory or none.
        '''
        return self._classes
