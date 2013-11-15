# -*- encoding: utf-8 -*-
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.musicexpressiontools.SetExpressionLookupExpression \
    import SetExpressionLookupExpression


class DivisionSetExpressionLookupExpression(SetExpressionLookupExpression):
    r'''Division set expression lookup expression.

    Definitions:

    ::

        >>> score_template = \
        ...     scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = \
        ...     musicexpressiontools.ScoreSpecificationInterface(
        ...     score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Example. Look up division set expression active at start of measure 4 in ``'Voice 1'``:

    ::

        >>> measure = red_segment.select_measures('Voice 1')[4:5]
        >>> set_expression = \
        ...     measure.start_offset.look_up_division_set_expression(
        ...     'Voice 1')

    ::

        >>> print format(set_expression)
        musicexpressiontools.DivisionSetExpressionLookupExpression(
            offset=musicexpressiontools.OffsetExpression(
                anchor=musicexpressiontools.MeasureSelectExpression(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=musicexpressiontools.CallbackInventory(
                        [
                            'result = self._getitem__(payload_expression, slice(4, 5, None))',
                            ]
                        ),
                    ),
                callbacks=musicexpressiontools.CallbackInventory(
                    []
                    ),
                ),
            voice_name='Voice 1',
            callbacks=musicexpressiontools.CallbackInventory(
                []
                ),
            )

    Lookup methods create division set expression lookup expressions.
    '''

    ### INITIALIZER ###

    def __init__(self, offset=None, voice_name=None, callbacks=None):
        SetExpressionLookupExpression.__init__(self, attribute='divisions',
            offset=offset, voice_name=voice_name, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate division set expression lookup expression.

        Returns payload expression.
        '''
        from experimental.tools import musicexpressiontools
        expression = self.offset.evaluate()
        offset = expression.payload[0]
        timespan_inventory = \
            self._get_timespan_delimited_single_context_set_expressions(
                self.attribute)
        time_relation = timerelationtools.offset_happens_during_timespan(
            offset=offset)
        candidate_set_expressions = \
            timespan_inventory.get_timespans_that_satisfy_time_relation(
                time_relation)
        root_specification = self.root_specification
        source_expression_set_expression = \
            root_specification._get_first_expression_that_governs_context_name(
                candidate_set_expressions, self.voice_name)
        assert source_expression_set_expression is not None
        expression = source_expression_set_expression.source_expression
        assert isinstance(
            expression, musicexpressiontools.IterablePayloadExpression)
        expression = self._apply_callbacks(expression)
        return expression
