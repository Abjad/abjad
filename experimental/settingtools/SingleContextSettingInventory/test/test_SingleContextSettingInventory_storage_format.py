from abjad.tools import *
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification
from experimental.settingtools import SingleContextSettingInventory


def test_SingleContextSettingInventory_storage_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    score_specification.interpret()

    setting_inventory_1 = segment.settings

    storage_format = setting_inventory_1.storage_format

    r'''
    settingtools.SingleContextSettingInventory([
        settingtools.SingleContextSetting(
            selectortools.SingleContextTimespanSelector(
                'Grouped Rhythmic Staves Score',
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='1'
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False,
            fresh=True
            )
        ])
    '''

    assert storage_format == "settingtools.SingleContextSettingInventory([\n\tsettingtools.SingleContextSetting(\n\t\tselectortools.SingleContextTimespanSelector(\n\t\t\t'Grouped Rhythmic Staves Score',\n\t\t\ttimespantools.SingleSourceTimespan(\n\t\t\t\tselector=selectortools.SegmentSelector(\n\t\t\t\t\tindex='1'\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False,\n\t\tfresh=True\n\t\t)\n\t])"

    setting_inventory_2 = eval(storage_format)

    assert isinstance(setting_inventory_1, SingleContextSettingInventory)
    assert isinstance(setting_inventory_2, SingleContextSettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
