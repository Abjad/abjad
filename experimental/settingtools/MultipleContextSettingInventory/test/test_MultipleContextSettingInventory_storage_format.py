from abjad.tools import *
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import library
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.selectortools.SingleContextCounttimeComponentSelector import SingleContextCounttimeComponentSelector
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextTimespanSelector import MultipleContextTimespanSelector
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


def test_MultipleContextSettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    storage_format = directive_inventory_1.storage_format

    r'''
    settingtools.MultipleContextSettingInventory([
        settingtools.MultipleContextSetting(
            selectortools.MultipleContextTimespanSelector(
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='1'
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False
            )
        ])
    '''

    assert storage_format == "settingtools.MultipleContextSettingInventory([\n\tsettingtools.MultipleContextSetting(\n\t\tselectortools.MultipleContextTimespanSelector(\n\t\t\tcontexts=['Grouped Rhythmic Staves Score'],\n\t\t\ttimespan=timespantools.SingleSourceTimespan(\n\t\t\t\tselector=selectortools.SegmentSelector(\n\t\t\t\t\tindex='1'\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(storage_format)

    assert isinstance(directive_inventory_1, MultipleContextSettingInventory)
    assert isinstance(directive_inventory_2, MultipleContextSettingInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
