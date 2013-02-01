from experimental import *
from experimental.tools.expressiontools import SetExpressionInventory


def test_SetExpressionInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    score_specification.interpret()

    set_expression_inventory_1 = \
        score_specification.specification.segment_specifications['red'].fresh_single_context_set_expressions
    storage_format = set_expression_inventory_1.storage_format
    set_expression_inventory_2 = eval(storage_format)

    assert isinstance(set_expression_inventory_1, SetExpressionInventory)
    assert isinstance(set_expression_inventory_2, SetExpressionInventory)
    assert not set_expression_inventory_1 is set_expression_inventory_2
    assert set_expression_inventory_1 == set_expression_inventory_2
