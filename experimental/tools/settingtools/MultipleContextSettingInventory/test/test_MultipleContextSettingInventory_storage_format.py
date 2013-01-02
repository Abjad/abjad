from abjad.tools import *
from experimental.tools import *
from experimental.tools.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.tools.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.tools.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.tools.timeexpressiontools.OffsetExpression import OffsetExpression
import py
py.test.skip('deprecated')


def test_MultipleContextSettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = score_specification['red'].multiple_context_settings
    storage_format = multiple_context_setting_inventory_1.storage_format
    multiple_context_setting_inventory_2 = eval(storage_format)

    assert isinstance(multiple_context_setting_inventory_1, MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
