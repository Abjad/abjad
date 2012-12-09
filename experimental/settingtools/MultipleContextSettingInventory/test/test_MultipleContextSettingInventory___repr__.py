from abjad.tools import *
from experimental import *
from experimental.requesttools.AbsoluteRequest import AbsoluteRequest
from experimental.symbolictimetools.SingleSegmentSymbolicTimespan import SingleSegmentSymbolicTimespan
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.symbolictimetools.SymbolicOffset import SymbolicOffset


def test_MultipleContextSettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = red_segment.multiple_context_settings
    multiple_context_setting_inventory_2 = eval(repr(multiple_context_setting_inventory_1))

    assert isinstance(multiple_context_setting_inventory_1, MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
