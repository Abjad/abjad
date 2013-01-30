from experimental import *
from experimental.tools.expressiontools.SingleContextSetExpression import SingleContextSetExpression
from experimental.tools.expressiontools.SetExpressionInventory import SetExpressionInventory
from experimental.tools.specificationtools.ScoreSpecification import ScoreSpecification


def test_SetExpressionInventory___repr___01():
    '''Repr is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    set_expression_inventory_1 = \
        score_specification.score_specification.segment_specifications['red'].single_context_set_expressions
    set_expression_inventory_2 = eval(repr(set_expression_inventory_1))

    assert isinstance(set_expression_inventory_1, SetExpressionInventory)
    assert isinstance(set_expression_inventory_2, SetExpressionInventory)
    assert not set_expression_inventory_1 is set_expression_inventory_2
    assert set_expression_inventory_1 == set_expression_inventory_2
