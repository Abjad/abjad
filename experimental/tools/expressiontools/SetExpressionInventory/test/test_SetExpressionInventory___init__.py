from abjad.tools import *
from experimental import *


def test_SetExpressionInventory___init___01():
    '''Init from other set expression inventory.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    set_expression_inventory_1 = score_specification['red'].single_context_set_expressions
    set_expression_inventory_2 = expressiontools.SetExpressionInventory(set_expression_inventory_1)

    assert isinstance(set_expression_inventory_1, expressiontools.SetExpressionInventory)
    assert isinstance(set_expression_inventory_2, expressiontools.SetExpressionInventory)
    assert not set_expression_inventory_1 is set_expression_inventory_2
    assert set_expression_inventory_1 == set_expression_inventory_2
