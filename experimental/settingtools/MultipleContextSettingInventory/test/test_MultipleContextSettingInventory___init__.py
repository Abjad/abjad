from abjad.tools import *
from experimental import *


def test_MultipleContextSettingInventory___init___01():
    '''Init from other multiple_context_setting inventory.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = red_segment.multiple_context_settings
    multiple_context_setting_inventory_2 = settingtools.MultipleContextSettingInventory(
        multiple_context_setting_inventory_1)

    assert isinstance(multiple_context_setting_inventory_1, settingtools.MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, settingtools.MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
