from abjad.tools import *
from experimental import *
from experimental.selectortools.SegmentItemSelector import SegmentItemSelector
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextTimespanSelector import MultipleContextTimespanSelector
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


def test_MultipleContextSettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = specificationtools.ScoreSpecification(score_template)

    segment = specification.append_segment()
    segment.set_time_signatures([(4, 8), (3, 8)])

    multiple_context_setting_inventory_1 = segment.multiple_context_settings
    multiple_context_setting_inventory_2 = eval(repr(multiple_context_setting_inventory_1))

    assert isinstance(multiple_context_setting_inventory_1, MultipleContextSettingInventory)
    assert isinstance(multiple_context_setting_inventory_2, MultipleContextSettingInventory)
    assert not multiple_context_setting_inventory_1 is multiple_context_setting_inventory_2
    assert multiple_context_setting_inventory_1 == multiple_context_setting_inventory_2
